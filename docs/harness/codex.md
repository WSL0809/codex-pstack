# Pstack in Codex

This is a compatibility adapter for the full upstream pstack, not a replacement workflow. Read it once per session before following any upstream skill. It changes only host-specific tools, models, paths, and authorization assumptions. Keep the original phases, prompts, principles, review contracts, tests, and output requirements.

The upstream snapshot and every adapter edit are recorded in `upstream/lock.json`, `upstream/pstack.zip`, and `migration.json`. The original Cursor vocabulary remains in the bodies so the engineering instructions can be compared directly with the source.

## Find the installed package

Resolve the selected SKILL.md path through symlinks before resolving relative references. `<pstack>` is the real directory containing `skills/`, `agents/`, `automations/`, and `docs/`. With a top-level skill it is three parent directories above the file. The installer stores a complete independent copy and links its skill directories into the discovery directory. Never search arbitrary private workspaces or select a package by guessed version.

If the user invokes `$pstack`, read `<pstack>/skills/poteto-mode/SKILL.md` in full. All 57 original skill names remain unchanged. `$pstack` is the sole extra alias. Benny's three operational skills remain dormant files, as in upstream; they are not registered as top-level skills.

Codex may qualify catalog names from the plugin manifest. CLI 0.160.0 exposes `codex-pstack:architect`, `codex-pstack:poteto-mode`, and `codex-pstack:pstack`. Use the catalog's actual name in user-facing invocation examples, such as `$codex-pstack:architect`. The base name and local skill directory remain `architect`; internal file-based routing is unchanged.

## Tools and calls

| Upstream instruction | Codex interpretation |
|---|---|
| `/name`, or “the **name** skill” | Read `<pstack>/skills/<name>/SKILL.md` and follow it. Use the actual catalog name when asking the user to invoke it, such as `$codex-pstack:name`. |
| `Task` | Use the agent delegation API exposed by this session, if authorized. Do not pass fields absent from its schema. |
| `AskQuestion` | Use the available question tool, respecting its mode restrictions. If absent, ask in normal conversation. Keep any explicit upstream checkpoint. |
| Open or update a todolist | Use the available plan/task tool. Otherwise maintain the same steps in a task file or concise status list. Preserve required steps and skip reasons. |
| `Read`, `Grep`, `Glob`, `Bash` | Use the available file/shell tools, `rg`, and `rg --files`. Resolve paths before use. |
| `create-skill` | Read the installed `skill-creator` skill. Preserve the user's requested fidelity rather than treating concision as permission to remove steps. |
| `control-ui`, `control-cli`, a browser skill | Use the available control skill that reaches the specified real surface. A source read is not a substitute for required runtime evidence. |
| Built-in PR tool | Use an available forge connector or authenticated CLI for the same operation. |

Discover capabilities from the current tools and installed skills. A name in upstream text does not install or authorize a tool. Do not invent a tool or call an undocumented service endpoint.

## Delegation and roles

The current session's delegation rules apply. If they require an explicit user request, honor that requirement. The upstream use of mandatory delegation cannot override a host restriction. Report an unavailable required independent check as blocked, not as completed by self-review. Use an upstream fallback only where the original workflow provides one. Continue independent steps that remain valid.

Map fields as follows:

- `subagent_type: poteto-agent`: use an available general worker role and give it the full absolute path to `<pstack>/agents/poteto-agent.md`, this adapter, and the original poteto-mode skill. Require it to read them before work. Do not register an unsupported custom agent type.
- `comment-sicko`: give a permitted read-only reviewer the full `<pstack>/agents/comment-sicko.md` prompt and this adapter. Preserve its review contract.
- `generalPurpose`: select an available general role. Do not infer capabilities from a role name.
- `readonly: true`: use a read-only role/sandbox if available, and state the no-write scope. If required isolation cannot be enforced, report that limit. `readonly: false` is not permission for unrelated writes.
- `environment: cloud`: use an actual authorized cloud capability when available. A local isolated worktree can substitute only when the task requires isolation rather than cloud-only state; disclose this substitution. If the remote runtime itself is necessary, the step is blocked.
- `run_in_background`, `resume`, `file_attachments`, `cloud_base_branch`: map only to supported fields or explicit brief instructions. A returned report is not proof a worker remains active.

Preserve the original role separation and fresh-agent rules. For every coding worker, name its owned paths and tell it it is not alone in the codebase and must preserve others' edits. Give each worker this adapter's absolute path; a prompt copied from a reference still needs the host mappings. A required independent model family remains unmet if all available agents inherit one model. Do not relabel that as cross-model agreement.

## Models and setup-pstack

Before model-dependent work, read `${CODEX_HOME:-~/.codex}/pstack/models.md` if it exists. This file is a pstack configuration read explicitly by these skills; it is not a Codex automatically loaded rules file. Keep upstream role labels and list semantics.

Map `~/.cursor/rules/pstack-models.mdc` and `pstack-models.mdc` to that file. Use `$setup-pstack` with these host changes:

1. Enumerate only model and effort values actually exposed by the current session. Do not assume Cursor model slugs work in Codex. If overrides cannot be detected, use `inherit-parent` and disclose the capability limit.
2. Preserve the existing role choices, budget question, complete role table, and user confirmation from the original steps. For a missing role, the Codex default is `inherit-parent`; do not silently substitute a different named model.
3. Map reasoning effort and speed only when the API supports them and current instructions permit overrides. Do not encode `-fast` or an effort suffix into an invented model name. Keep unavailable budgets or model diversity explicit.
4. Write the original comment and role-line format to `pstack/models.md`, without `.mdc` frontmatter. Do not edit `config.toml`, AGENTS.md, or global model settings. Offer the original verification-skill follow-ups.

`auto` and `inherit-parent` mean omit a model override. Original literal model names describe the upstream configuration; they are not availability claims. If a required model is unavailable, retain the role and report the substitution or blocked requirement.

## Paths, history, and persistent state

| Upstream path or concept | Codex interpretation |
|---|---|
| `.cursor/skills/` | The target project's `.agents/skills/` |
| `~/.cursor/skills/` | User skill discovery directory, normally `~/.agents/skills/` |
| `~/.cursor/plugins/`, highest plugin version search | The already resolved `<pstack>` installation; use explicit paths |
| `.cursor/rules/*.mdc` | Read applicable AGENTS.md and existing Codex instructions. Do not create translated global rules without a request. The pstack model file has the explicit mapping above. |
| Current agent's store | The task's existing durable store. If none exists and persistence is required, create a task-scoped directory in the project, such as `.pstack/tasks/<slug>/`. |
| `agent-transcripts/` or a Cursor chat URL | Current conversation, a user-supplied export, or the session's authorized history interface. Use a digest only where the original skill permits it. |
| Upstream GitHub link to a bundled file | Read the corresponding local file first. The original URL remains an attribution or external reference. |

Do not glob private session roots or unrelated repositories. Do not fabricate a transcript path. If a required transcript or remote artifact cannot be accessed, state exactly what is missing.

Run bundled helpers from their actual `<pstack>` path. Install Bun/Node dependencies in a writable task copy when necessary, rather than changing the installed package. Preserve package manifests and lockfiles. Node, Bun, GitHub CLI, TLA+, Java, a simulator, and private connectors are separate prerequisites; the skill package does not supply them.

The orchestration CLI accepts `--store` or `ORCH_STORE`; point it at the task store. The worktree audit has one narrow executable adaptation: it reads only an explicitly supplied `PSTACK_TRANSCRIPTS_DIR`. With no history directory it marks otherwise safe candidates `review-no-history`. A missing activity source is not evidence of inactivity. Verify current ownership before deleting any worktree. The original shell audit also uses macOS-oriented `stat` and `date` commands; validate their output on another OS and do not rely on an unavailable history column.

## Host-only features and long runs

Cursor `/loop`, automations, routine wakes, `update_state`, `SendToUser`, and dashboard controls have no assumed Codex equivalent. Use a current documented capability only when it satisfies the same requirement and the user has authorized it. Otherwise mark the step unavailable and preserve its acceptance condition. If it is essential, the result remains incomplete. Do not claim that local files install a scheduler or that work continues after this session ends.

Existing Bugbot comments are ordinary review evidence. Starting or configuring Bugbot requires that service. For `make-bot-ui`, preserve the webhook, identity, secret handling, and network requirements, but do not invent a Codex webhook service. For Benny, read [codex-benny.md](codex-benny.md) and preserve all original thread-safety gates.

## Authorization

Follow the current system, developer, user, and repository instructions. The original statements about “Just do it”, automatic backlog tickets, messages, PRs, commits, merges, deployment, or session overrides do not create permission. Perform actions already requested or authorized without asking again. A broader task does not authorize unrelated external writes.

Keep original review-only and explicit checkpoints. Do not use a pause as a reason to commit or push without authorization. For unsupported or unauthorized steps, report the precise gap and continue work that does not depend on it. Do not weaken a test, skip an independent gate silently, or replace the original playbook to make a task appear complete.
