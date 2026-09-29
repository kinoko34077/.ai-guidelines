# Durable Progress Policy

## Purpose

For GitHub-backed agent work, recoverable progress is a required execution property rather than optional reporting hygiene.

The goal is to prevent interruption from forcing speculative reconstruction, duplicated accepted work, or unnecessary full re-verification.

For managed repositories, live devflow remains authoritative for exact Session/cursor/review/collision semantics. This document defines the shared static rule that agents must externalize progress before substantive multi-step work continues.

## Priority

Within already-authorized work:

```text
Safety / explicit Human gate
> durable progress externalization
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
4. then start the next unit.

Do not defer all progress writing until the end of the chat or until a user-facing status response.

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

For managed repositories, consult live `kinoko34077/devflow` for the current detailed resume, Session, cursor, takeover, review, and collision contract.

## Chat behavior

Chat may summarize the current result and need not duplicate the full progress ledger. Chat brevity is never permission to skip durable GitHub externalization.
