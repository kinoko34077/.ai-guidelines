# AI Agent Bootstrap Policy

## Purpose

This policy defines how Codex, Claude Code and other development agents decide when to leave static shared guidelines and consult live KiNoTch development state.

It is intentionally a routing policy. It must not mirror mutable Work Status, Audit SHA, Active Work, blockers, run IDs, Sync Health values or other Current State from devflow.

## Authority model

For KiNoTch managed repositories:

- `kinoko34077/devflow` is the cross-repository operational authority.
- The owning repository is the detailed technical authority for its requirements, specifications, Current State, Issues/PRs, code and tests.
- `.ai-guidelines` is the shared static policy authority for coding, specification, UI/UX and usability rules.
- GitHub Project is display/overview only and is not canonical.

If these layers disagree, do not use `.ai-guidelines` or GitHub Project to overwrite live repository state. Read the owning repository, then reconcile devflow if its cross-repository summary is stale.

## When live devflow is required

Before answering or acting on any of the following for a managed repository, consult live devflow:

- current repository state;
- implementation state or readiness;
- continuation/resume or “where did we leave off?”;
- audit or re-audit;
- implementation or bug-fix work;
- review, merge readiness or verification status;
- Issue / Pull Request / Work Order state;
- blocker / Next Action / Priority / Risk;
- cross-repository work;
- devflow / Project-sync control-plane work itself.

Static coding/spec/UI policy questions that do not depend on a repository's live state do not require a devflow lookup.

## Required bootstrap sequence

When the KiNoTch Devflow MCP is connected:

1. call `bootstrap_repository` with the current `kinoko34077/<repo>` name;
2. read the returned Repository Control state;
3. follow its Canonical Entry Points in the owning repository;
4. open the active owning-repository Issue / Work Order / PR when referenced;
5. inspect only the task-relevant specs / Current State / code / tests;
6. then apply the relevant `.ai-guidelines` policy for the actual implementation/review task.

If the MCP is unavailable but GitHub is available, perform the same sequence directly from live `kinoko34077/devflow/AGENTS.md` and the exact open `[REPO] <repo>` Control Issue.

If live devflow/GitHub cannot be read, do not infer Current State from chat history, old summaries or these static guidelines. Mark the live state as unverified and limit work accordingly.

## Reporting

Use Issue-first reporting:

- durable implementation detail, findings, verification evidence, blockers and handoff go to the appropriate owning Issue;
- cross-repository summary changes go to the devflow Repository Control / Work Order;
- chat output remains a concise result/current-state/blocker/user-action/Issue-reference summary unless detailed explanation is explicitly requested.

## Safety boundary

The devflow MCP is expected to be read-only. Static guideline routing must not silently authorize release/deployment, destructive deletion, shared-history rewrite, credential/session/permission changes or other security-sensitive actions.
