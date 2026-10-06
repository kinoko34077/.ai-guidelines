# Durable Progress Policy

## Purpose

For GitHub-backed agent work, recoverable progress is a required execution property rather than optional reporting hygiene.

The goal is to prevent interruption from forcing speculative reconstruction, duplicated accepted work, unnecessary full re-verification, or stale durable records that contradict an already accepted state transition.

For managed repositories, live devflow remains authoritative for exact Session/cursor/review/collision semantics. This document defines the shared static rule that agents must externalize progress before substantive multi-step work continues and must reconcile the finite durable surface set directly affected by their own accepted transition before leaving that bounded unit.

## Priority

Within already-authorized work:

```text
Safety / explicit Human gate
> durable progress externalization and affected-surface reconciliation
> throughput / shortest-path / convenience / chat concision
```

This rule does not weaken release/deploy/publication, destructive, credential/session/permission, shared-history, security, review, or other Human-gated boundaries.

## Mandatory progress surface

When a GitHub repository exists and work involves mutation, implementation, review, verification, audit, investigation, multiple recovery-relevant actions, or meaningful interruption/reconstruction cost, create or reuse one durable GitHub progress surface before substantive continuation.

Accepted surfaces include:

- the owning Issue / Work Order;
- a trusted Issue / Work Order comment;
- a bounded dedicated progress Issue/ledger when that improves recovery;
- other live-devflow-approved task progress surfaces.

Do not create one Issue per checkpoint. Prefer one surface per bounded operation unless independent completion/handoff/acceptance requires decomposition.

A single-step read-only lookup with no continuation/recovery value may be exempt. If it grows beyond that boundary, externalize progress before continuing.

## Minimum recoverable state

The durable surface must make it possible to recover:

- scope and explicit exclusions;
- latest completed checkpoint;
- first unfinished action;
- branch / PR / exact head when applicable;
- blocker;
- compact evidence references when relevant.

Field names may follow repository-local policy. The information itself is mandatory.

## Update ordering

Before beginning the next materially distinct recovery unit:

1. finish the current bounded unit;
2. write its result/checkpoint to the durable GitHub surface;
3. record the first unfinished next action;
4. reconcile the durable surfaces directly affected by the accepted state transition when they would otherwise become stale or contradictory;
5. run the global replan / termination gate against the original objective, current acceptance and live evidence, explicitly choosing `CONTINUE / CHANGE_PATH / SPLIT / HOLD / STOP`;
6. start the next unit only when continued work directly serves an unmet acceptance condition, a concrete defect/safety boundary, or an explicit user request.

Do not defer all progress writing or reconciliation until the end of the chat or until a user-facing status response. A durable checkpoint is also a decision boundary: if acceptance is already satisfied, complete only the minimum required reconciliation and stop.

## Affected-surface reconciliation before exit

A worker that causes an accepted state transition owns the cleanup of the finite durable surface set made stale, contradictory, or concretely suspect by that transition.

Before moving to the next materially distinct unit, or before leaving the task as `DONE`, `RELEASED`, `HANDOFF`, `WAITING`, or equivalent, inspect the directly affected surfaces as applicable. Typical examples include:

- owning Issue / Work Order status, blocker and Next Action;
- durable progress ledger / checkpoint;
- active Execution Session state;
- branch / PR / accepted exact head references;
- parent, child or dependency Issues whose current routing changed;
- active-work, candidate, supply or routing projections that still advertise retired work;
- repository Current State when accepted repository-level state changed;
- specification / ADR when accepted durable requirements or design changed;
- Repository Control when the cross-repository summary changed.

This is **not** a requirement to sweep every Issue or repository after each task. The inspection is bounded to surfaces that the current transition directly changed or gave a concrete reason to suspect are stale.

If an in-scope stale status, resolved blocker, obsolete routing reference or contradictory current-state projection can be corrected safely within existing authority, correct it before leaving the bounded unit.

Do not take over another active worker's semantic scope, cross a Human/security/permission gate, or absorb an independent unrelated defect merely because it was noticed during cleanup. Record a durable finding/reference for the owning task instead.

A bounded unit is not operationally complete until its accepted result, recovery checkpoint, and directly affected durable projections agree. Cross-repository or periodic consistency audits remain a backstop for missed drift and interaction defects; they are not the normal garbage collector for producer-owned stale state.

## Working notes

The same temporary progress surface may hold concise scratch material such as:

- `NOTE`;
- `HYPOTHESIS`;
- `UNVERIFIED` observations;
- partial findings;
- failed-path notes;
- command/run/artifact references.

Label provisional material so it cannot be mistaken for accepted specification, Current State, formal finding, or verification evidence. Promote accepted durable information to its owning canonical surface.

## Missing or stale progress

If qualifying work has no usable progress surface, or the last completed / first unfinished boundary is ambiguous, treat that as an operational defect to repair before broad continuation.

Do not invalidate existing artifacts. Instead, inspect live Issue/branch/PR/head/check/Review evidence only as far as needed to reconstruct the position, establish or repair the progress surface, then continue from the resolved first unfinished unit.

Chat history, summaries, and Memory are not substitutes for this repair.

## Resume behavior

Resume from the latest durable checkpoint. Do not repeat already accepted setup, verification, implementation, review, or other bounded units solely because the previous chat/provider context disappeared.

Re-observe or re-verify only volatile or changed state, or a concrete inconsistency/missing-evidence boundary.

For managed repositories, consult live `kinoko34077/devflow` for the current detailed resume, Session, cursor, takeover, review, collision, and affected-surface reconciliation contract.

## Chat behavior

Chat may summarize the current result and need not duplicate the full progress ledger. Chat brevity is never permission to skip durable GitHub externalization or affected-surface reconciliation.