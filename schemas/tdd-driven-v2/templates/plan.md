# Execution Plan: {{change_name}}

## Micro-tasks

### Step 1: RED — [description]

- Test file: `[path]`
- Assertion: [what to test]
- Expected failure: [reason]
- Verify: `npm test -- [test-file]`
- Evidence: Test MUST fail with "[expected reason]"

### Step 2: GREEN — [description]

- Pass test from: Step 1
- Minimal code: [what to implement, file path]
- Verify: `npm test -- [test-file]`
- Evidence: Test MUST pass

### Step 3: REFACTOR — [description]（可选）

- Clean up: [what to refactor]
- Verify: `npm test`
- Evidence: ALL tests MUST still pass

<!-- Repeat pattern for each task in tasks.md -->

---

## Execution Mode Selection

REQUIRED: Use superpowers:subagent-driven-development skill for execution.
DO NOT use executing-plans or inline execution.
Reason: Atomic TDD tasks require subagent isolation. Each task is a single TDD phase — one subagent per phase.
