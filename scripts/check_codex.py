#!/usr/bin/env python3
"""Ask a local Codex app-server to discover the installed user skills in two directories.

Uses the initialize and skills/list protocol exposed by Codex CLI 0.160.0.
Does not create a model session or run a model request.
"""

import json
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time

EXPECTED = {"pstack", "pstack-design", "pstack-debug", "pstack-review", "pstack-verify", "pstack-explain", "pstack-improve", "pstack-orchestrate"}


def check():
    version = subprocess.run(["codex", "--version"], check=True, capture_output=True, text=True, timeout=10).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="pstack-discovery-") as other:
        process = subprocess.Popen(["codex", "app-server", "--stdio"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        messages = queue.Queue()

        def read():
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except ValueError:
                    continue
            messages.put({"closed": True})

        reader = threading.Thread(target=read, daemon=True)
        reader.start()

        def send(message):
            process.stdin.write(json.dumps(message) + "\n")
            process.stdin.flush()

        def receive(request_id):
            deadline = time.monotonic() + 20
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise RuntimeError("Codex discovery timed out")
                try:
                    message = messages.get(timeout=remaining)
                except queue.Empty:
                    raise RuntimeError("Codex discovery timed out") from None
                if message.get("closed"):
                    raise RuntimeError("Codex app-server closed before discovery completed")
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(str(message["error"]))
                    return message["result"]

        try:
            send({"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "pstack_discovery", "version": "0.1.0"}}})
            receive(1)
            send({"method": "initialized"})
            send({"id": 2, "method": "skills/list", "params": {"cwds": [str(Path.cwd()), other], "forceReload": True}})
            response = receive(2)
            entries = response["data"]
            if len(entries) != 2:
                raise RuntimeError("Expected discovery results for both directories")
            rows = []
            for entry in entries:
                ours = [skill for skill in entry["skills"] if skill["name"] in EXPECTED]
                if {s["name"] for s in ours} != EXPECTED or len(ours) != len(EXPECTED):
                    raise RuntimeError("Missing or duplicate pstack skill names in a workspace")
                if not all(s["enabled"] and s["scope"] == "user" for s in ours):
                    raise RuntimeError("Pstack skills were not all enabled at user scope")
                if any("pstack" in error["path"] for error in entry["errors"]):
                    raise RuntimeError("Codex reported a pstack skill parse error")
                rows.append({"workspace": "isolated" if entry["cwd"] == other else "current", "skills": sorted(s["name"] for s in ours), "scope": "user", "enabled": True})
            return {"codex": version, "results": rows}
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            process.stdin.close()
            reader.join(timeout=1)
            process.stdout.close()


if __name__ == "__main__":
    try:
        print(json.dumps(check(), indent=2))
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"pstack discovery: {error}", file=sys.stderr)
        sys.exit(1)
