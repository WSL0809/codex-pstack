# Codex adapter

## Authority and capability

Follow the current system, developer, user, and repository instructions. This package supplies workflows, not extra permissions. A request to continue autonomously does not remove an approval boundary. If an action is unavailable, report the limit and continue independent work that remains useful.

Inspect the tools actually exposed by the session. Prefer installed skills and purpose-built connectors when suitable. Use shell tools for local code, Git, and project checks. Read the relevant browser skill before operating a browser. Do not assume a browser, GitHub connector, cloud runtime, transcript reader, scheduler, or formal verifier exists.

Do not invent APIs or require a specific model family. Use the configured model. Use a model override only when authorized and supported by the current runtime. A tool name appearing in upstream documentation is not evidence it exists here.

## Collaboration

Use subagents only when the session permits delegation and the task benefits from independent work. If a policy requires an explicit user request, follow it. These skills do not override that requirement. Do not launch nested CLI sessions to work around a delegation restriction.

When delegation is available, use the runtime's documented agent API. Give every worker a goal, exact write scope, context pointers, acceptance criteria, verification command, and required report. Tell workers they are not alone in the codebase and must preserve others' edits. Isolate conflicting writes with separate worktrees or a single writer. Keep the integration owner explicit.

Independent reviewers should receive the goal, artifact, and necessary context without the author's preferred conclusion. Distinct sessions are not proof of independent model families. Label the review accurately. Without delegation, do a separate review pass after implementation and state that it was a self-review. Run independent shell reads concurrently when useful; mutations and dependent steps remain ordered.

## Paths and state

Treat installed skill directories as read-only resources during normal use. Resolve references from the installed SKILL.md path. All eight skills are installed together because they share these relative references.

Keep project results in the user's project. Do not write task progress into the installed package. Use an existing project planning location; otherwise use a task-specific directory such as `.pstack/tasks/<task-name>/` for long work. Do not create persistent tracking files for trivial tasks. Do not collect secrets in evidence logs.

Use only the current conversation, a user-provided transcript, an explicitly exposed history tool, or the task's own handoff. Do not scan other workspaces or private session stores. A local installation does not make skills available to remote machines or cloud sandboxes. Install them there or include the package in that repository.

## Scheduling and external actions

Continue while the active session can make progress. Do not promise that a skill alone runs after the session ends. Use a scheduler only if available and requested. Write a checkpoint before ending an incomplete long task.

Do not send chat messages, create tickets, publish, or merge simply because an upstream workflow mentions them. Execute actions already authorized by the task; otherwise deliver the concrete local result. Do not repeatedly ask for permission already granted.
