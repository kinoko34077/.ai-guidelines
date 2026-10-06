# KiNoTch. GitHub Development — Shared Operating Rules

## Purpose and authority

This policy gives Codex, Claude Code and other development agents the shared static operating rules for KiNoTch. GitHub development.

It is a durable policy summary, not a second copy of live development state or detailed devflow lifecycle semantics.

For managed repositories:

- live `kinoko34077/devflow` is the cross-repository operational authority;
- the owning repository is the detailed technical authority for its requirements, specifications, Current State, Issues/Work Orders, Pull Requests, code and tests;
- this file defines shared static GitHub operating principles;
- GitHub Project is a derived display/overview layer and is never canonical.

When detailed Session, Review, merge, takeover, collision, audit or state semantics are needed, follow the current live devflow canon. Do not freeze mutable Work Status, Audit SHA, Active Work, blockers, run IDs or similar current-state values into this file.

## 1. Use live GitHub as the source of truth

For current state, resume position, Issue/PR state, Review state and implementation status, do not infer from chat history, old summaries or memory when live GitHub is available.

For a managed repository, read in this order:

1. live `kinoko34077/devflow/AGENTS.md` or the equivalent Devflow MCP bootstrap result;
2. the exact open devflow `[REPO] <repository>` Control Issue;
3. the owning repository's canonical entry points;
4. the active owning-repository Issue / Work Order / PR and task-relevant Current State, specifications, code and tests.

## 2. Keep responsibilities separated

Use devflow for cross-repository state, Work Orders and common operational control. Keep detailed requirements, implementation, findings, verification and repository-specific decisions in the owning repository.

GitHub Project is an overview surface only. Do not treat Project fields as authority over canonical Issues or repository state.

## 3. Record durable work Issue-first

Put implementation detail, findings, blockers, verification evidence, Next Action, handoff information and user-decision requirements on the appropriate owning Issue / Work Order / PR according to live devflow rules.

Do not make chat history the only recovery record for non-trivial work.

For qualifying work also apply `guidelines/DURABLE_PROGRESS_POLICY.md`, including its rule that the worker causing an accepted state transition reconciles the directly affected durable surfaces before leaving the bounded unit.

### Material-boundary global replan

The compact invariants in `guidelines/AI_AGENT_BOOTSTRAP_POLICY.md` apply throughout GitHub work, not only at startup.

After each materially distinct checkpoint, on a tool/execution-path switch, and before optional extra verification or surrounding reconciliation, re-evaluate the original objective, current acceptance state, unresolved correctness/safety gaps and live evidence. Explicitly choose `CONTINUE / CHANGE_PATH / SPLIT / HOLD / STOP`.

Do not continue because another operation is merely related, available, cleaner, or potentially useful. Another material unit must directly serve an unmet acceptance condition, a concrete defect/safety boundary, or an explicit user request. When acceptance is satisfied, reconcile only the finite directly affected durable surfaces and stop.

Prefer repository/GitHub-native execution and evidence surfaces. Repeated friction in an indirect or alternate tool route is a reason to change paths or leave a durable handoff, not to build more ceremony around that route.

## 4. Use a dedicated branch and Pull Request for normal changes

For normal changes, do not write directly to the default branch.

Before mutation, verify the relevant current SHA, existing Issue/PR state and overlapping work. Use a dedicated branch, perform the task-relevant tests/regression/real-entry verification, and expose the resulting diff through a Pull Request.

## 5. Proceed autonomously for already-authorized, safe and reversible changes

Additional user confirmation is not required when all of the following are true:

- the change remains inside an already-authorized scope;
- current live state and applicable policy have been checked;
- no blocking finding or unresolved required review/check remains;
- required verification is current for the exact change/head being accepted;
- catastrophic or irreversible risk is low;
- the change can be safely restored through a normal revert/rollback Pull Request;
- the operation does not cross a confirmation-gated boundary in section 7 or a stricter repository/task-specific rule.

When these conditions hold, the agent may continue through implementation, Formal Review and merge without pausing merely to request an extra human bridge step.

## 6. Leave Formal Review on non-trivial Pull Requests

Every non-trivial Pull Request requires a durable Formal Review under the current devflow review protocol.

An implementer-authored Formal Review is normally a valid review path. A different reviewer is **not required by default**.

A different reviewer becomes mandatory when the current owning task or live devflow requires it. Shared escalation boundaries include:

1. the owning Issue / Work Order explicitly requires a different reviewer;
2. security, authentication, credential, permission or privacy boundaries change materially;
3. destructive or difficult-to-reverse state/data migration is involved;
4. persistent schema/data migration creates non-trivial unrecoverable loss or corruption risk;
5. a public/shared contract has a breaking or high-impact compatibility change;
6. one semantic change propagates across multiple repositories/consumers and rollback is not purely local;
7. devflow authority, merge safety or source-of-truth semantics change materially;
8. a prior Review finds a P0/P1 issue whose resolution warrants independent confirmation;
9. the user explicitly requests another reviewer.

Priority, repository identity or a broad risk label alone do not automatically create reviewer-independence when the actual change does not cross one of the applicable escalation boundaries.

The live devflow review specification remains authoritative for exact-head review evidence, Review Provenance, finding severity, blocking conditions and review outcomes.

## 7. Require explicit user confirmation for high-risk or externally consequential operations

Do not execute the following without explicit user confirmation:

- release or deploy;
- external publication or another action with material external effect;
- destructive deletion;
- shared-history rewrite or force-style rollback of shared history;
- credential, session or permission changes;
- other security-sensitive operations;
- other operations that are materially difficult to reverse safely.

Narrow authorization for one such operation does not authorize adjacent security-sensitive or irreversible actions.

## 8. Recover by adding history, not rewriting shared history

If a merged change proves wrong, use a dedicated rollback branch and revert/rollback Pull Request when that is a safe recovery path.

Do not use shared-main history rewriting or force-style rewind as the normal recovery mechanism.

## 9. Leave recoverable state for interruption and timeout

For non-trivial work, follow the live devflow Manual Execution Session protocol and keep the owning Issue / Work Order recoverable from GitHub evidence.

Record bounded scope, provenance, branch/PR, latest completed checkpoint, first unfinished Next Action and blocker state at recovery-relevant milestones.

For the current manual stale convention, `CLAIMED` / `RUNNING` sessions are only stale candidates after the live devflow-defined inactivity condition is satisfied; do not invent a shorter timeout from chat disappearance alone.

### 9.1 Reconcile directly affected durable surfaces before exit

The worker that produces an accepted transition is responsible for reconciling the finite set of durable records that transition directly made stale, contradictory or concretely suspect.

Before moving to the next materially distinct unit or leaving as `DONE`, `RELEASED`, `HANDOFF`, `WAITING`, or equivalent, inspect the applicable affected surfaces, such as:

- owning Issue / Work Order status, blocker and Next Action;
- progress ledger and Session state;
- branch / PR / accepted exact-head references;
- parent/child/dependency Issue routing;
- active-work, candidate, supply or routing projections;
- Current State, specification or ADR only when the accepted transition changed information they own;
- devflow Repository Control only when the cross-repository summary changed.

Do not turn this into a global sweep. The affected set is bounded to surfaces the current transition changed or gave a concrete reason to suspect are stale.

Correct safe in-scope stale state before exit. If the stale surface belongs to another active worker, requires Human/security/permission authority, or is an independent unrelated defect, do not take it over; leave a durable finding/reference for its owner.

Cross-repository consistency audits are a backstop for missed drift and interaction defects, not the routine cleanup owner for state made stale by the producing worker.

## 10. Resume interrupted work from live evidence

A new agent should inspect the owning Issue / Work Order, relevant Session Record, branch/PR, current head and CI/Review evidence before deciding whether to continue, hand off, wait, integrate or take over.

The previous agent's chat narrative is not required for recovery and must not override newer live evidence.

## 11. When stopping for safety, leave a recovery path

If evidence is insufficient, state conflicts, or a required condition cannot be verified, do not guess and continue.

Record the blocker, missing evidence, resume condition and concrete Next Action on the owning durable record so a later worker can continue without reconstructing the situation from chat.

Reconcile any directly affected surfaces that can be updated safely without crossing the blocker; do not leave avoidable stale routing behind merely because the primary task is waiting.

## 12. Ask the user only when human judgment or confirmation is actually required

Do not ask the user to manually bridge ordinary CI waiting, normal Formal Review, merge-readiness determination, safe reversible merge, agent-timeout recovery, ordinary verification, or routine affected-surface reconciliation when existing rules, available tooling and objective evidence are sufficient to decide the next action.

### Machine-verifiable checks are agent-owned

When a required check can be observed, measured or reproduced with tools available to the agent or implementation environment, the agent should perform that check directly before asking the user to do it.

Examples include, when applicable:

- running repository-owned tests, builds, linters, benchmarks or smoke checks;
- reading logs, API responses, process state or generated artifacts;
- exercising the real CLI/API/GUI/Web entry point;
- driving a browser through supported automation or DevTools interfaces;
- reading DOM, network, performance, layout, accessibility-tree or runtime metrics;
- checking filesystem/repository state that is directly available to the authorized environment.

Do not convert a machine-verifiable check into a generic human handoff merely because a user could also inspect it manually. In particular, avoid requests such as “open F12 and report the value”, “confirm visually that it seems smooth”, or “try it and tell me whether it works” when the relevant property can be obtained directly through available instrumentation or reproducible automation.

Verification evidence should identify the actual source of the conclusion: command/check, exact SHA or artifact when relevant, measured value or observed state, comparison rule/threshold when one exists, and the resulting pass/fail or equivalent conclusion. Do not replace evidence with the agent's subjective statement that something “looks good”.

Human verification remains appropriate when the unresolved property genuinely depends on:

- human preference or product/specification choice;
- subjective perception that is itself the requirement and is not adequately represented by objective proxies;
- a physical or external state unavailable to authorized tooling;
- end-to-end assistive-technology or device behavior that the available environment cannot actually exercise;
- explicit safety, authority or confirmation boundaries requiring a human decision.

When such a boundary remains, state it narrowly. Do not use a broad “human verification required” label to cover nearby checks that are mechanically verifiable.

Ask the user when:

- section 7 requires explicit confirmation;
- the owning task explicitly reserves a decision for the user;
- multiple valid product/specification choices require human preference rather than evidence;
- authority or requirements genuinely conflict and no canonical source resolves them;
- proceeding would require expanding beyond the already-authorized scope;
- the remaining acceptance property falls into one of the genuinely human-only boundaries above and no authorized machine evidence can establish it.

The purpose of this rule is to remove unnecessary human relay work without weakening safety, review, provenance, verification quality or source-of-truth boundaries.