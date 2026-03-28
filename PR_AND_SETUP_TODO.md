# PR and Setup TODO

## Parked (Do After PR Sweep)
- [ ] Confirm preferred Context7 mode in Codespace (MCP Server as default, Relay as fallback).
- [ ] Verify only one Context7 extension is active during normal work.
- [ ] Run a quick Context7 smoke test in Copilot Chat (ask for version-specific docs/examples).
- [ ] Save the working setup in workspace notes/settings so it is repeatable.

## PR Triage Workflow (Next Task)
- [ ] Gather open PR list with status (author, age, CI state, mergeability).
- [ ] Prioritize PRs into: quick merge, needs review, blocked.
- [ ] For each PR, check scope vs. title and confirm no hidden unrelated changes.
- [ ] Run/verify relevant checks for each PR (tests, lint, script validation if applicable).
- [ ] Review for regressions first: behavior changes, data assumptions, breaking renames, missing docs.
- [ ] Leave review notes with clear action items and severity.
- [ ] Merge only green + approved PRs; label or comment blocked PRs with exact unblock condition.
- [ ] After each merge, pull/rebase and resolve conflicts immediately before opening the next review.

## Per-PR Checklist
- [ ] Read PR description and linked issue/context.
- [ ] Inspect file diff for risky areas (core scripts, data transforms, workflow files).
- [ ] Validate naming, folder placement, and consistency with repo structure.
- [ ] Verify docs/readme updates for user-facing changes.
- [ ] Confirm CI/checks status and required approvals.
- [ ] Decide: approve, request changes, or close.

## End-of-Session Wrap
- [ ] Update changelog/release notes if needed.
- [ ] Post a summary comment with merged PRs and deferred follow-ups.
- [ ] Revisit the parked Context7 setup checklist.
