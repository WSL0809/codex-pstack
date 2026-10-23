# Worktree cleanup

Only clean up resources in the requested scope. Inventory worktrees, branches, disk usage, uncommitted and untracked files, active processes, and remote merge state before removal.

A branch merged by squash may not be an ancestor of trunk. Verify the actual PR outcome and patch content before calling it disposable. A merged branch with new unpushed commits still contains work. A lock or running session can indicate an active owner.

List exact paths, evidence that each is disposable, and unresolved ownership. Follow existing authorization for deletion. Do not infer that every stale directory is abandoned, use force removal to overcome a warning, or delete unrelated simulators and caches. Preserve uncertain work. After authorized removal, inspect the worktree registry and remaining paths.
