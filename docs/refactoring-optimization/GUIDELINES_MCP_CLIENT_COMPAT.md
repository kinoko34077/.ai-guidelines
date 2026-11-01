# Guidelines MCP — existing-client compatibility and source verification

**Owner:** [Issue #32](https://github.com/kinoko34077/.ai-guidelines/issues/32).
**Authority:** the actual Markdown at
`guidelines/REFACTORING_OPTIMIZATION_STANDARD.md` on the current main.
This guide documents read-only retrieval and diagnostics. It does not grant
permission to install/reconfigure client integrations, adjust credentials,
wake an external agent, or make a paid API call.

## Why the Codex read failed

The v1.0 specialist policy and the `refactoring` / `optimization` routes
are already implemented in `guidelines_mcp.py` (PR #33). A real Codex
environment nevertheless rejected both `get_guidelines_for_task(task_type=...)`
calls at tool-input validation. A GitHub code update does **not** refresh
a client-registered tool schema or guarantee that an already-started
process uses the latest checkout. The observed rejection establishes
client/server schema divergence, **not** which installation, process, or
tool-schema cache is stale. Do not edit policy content merely to address it.

## Read-only decision procedure, in order

1. Fetch live devflow + owning repository sources first. For an existing-code
   improvement, obtain the **actual complete specialist Markdown** before
   establishing a baseline or changing code.
2. If the Guidelines MCP is connected, call `check_setup()` and
   `get_bootstrap()`. Verify the server/version, `root`, `ready`,
   `available_task_types`, and the `specialist_standard` source identity
   when those fields exist. As of server 1.1.1, `specialist_standard`
   contains `available`, byte count and SHA-256 of the **local file bytes**.
   Compare the hash with the independently fetched intended Markdown bytes;
   neither a version number nor the presence of a filename alone proves
   current content. Missing fields mean an older server **or** old result
   format; do not assume source freshness.
3. On a current tool schema, call
   `get_guidelines_for_task(task_type="optimization")` or
   `get_guidelines_for_task(task_type="refactoring")`. Confirm the returned
   `documents` include the exact `guidelines/REFACTORING_OPTIMIZATION_STANDARD.md`,
   `missing` is empty, both `truncated` flags are false and file contents
   match the authoritative revision.
4. If the task-type enum is rejected **by the client** or the tool is absent,
   attempt the **existing** backward-compatible MCP tool:
   `read_guideline(relative_path="guidelines/REFACTORING_OPTIMIZATION_STANDARD.md")`.
   Confirm full content / `truncated=false` and verify against the canonical
   GitHub original. A stale server can lack that newly added file or return
   old bytes; a successful API response is not by itself a revision proof.
5. If the MCP is unavailable, inaccessible, truncated, or mismatched, use
   [the canonical GitHub Markdown](https://github.com/kinoko34077/.ai-guidelines/blob/main/guidelines/REFACTORING_OPTIMIZATION_STANDARD.md)
   through the existing authorized GitHub reader. Clearly record:
   `MCP specialist route: FAIL/UNVERIFIED`, `GitHub source: PASS` when
   independently verified. This fallback permits ordinary authorized work;
   it does not mark the MCP acceptance as passed.

## Diagnosing a real client mismatch

Collect **only non-secret** evidence from that running client: its exposed
tool input schema, `check_setup` and `get_bootstrap` results if available,
server command target and root **without credentials**, whether the actual
process has been restarted, exact policy source SHA-256, and error stage
(client validation vs server response). Do not paste tokens or private paths
into a public Issue; redact machine-specific local paths when recording.

- Old enum plus current `check_setup`/source fingerprint: likely cached client
  schema; **not proven** until the client refresh is performed and retested.
- Old enum plus old server version/missing source: old process/checkout/target
  remains possible; inspect the already authorized deployment target.
- New enum with missing/truncated policy: content/root or return-limit issue.
- New enum and matching full Markdown via a real client call: that client's
  specialist read path passes. Other clients remain separately unverified.

**Client re-registration, restart, tool-permission changes, or credential
changes are not performed by this document or by CI.** Use the supported
client-specific configuration workflow after separately checking the change
authority. Do not create a duplicate MCP server as a shortcut.

## Verification surfaces

- `python -m unittest discover -v -p "test_guidelines_mcp_security.py"`:
  pure routing and filesystem containment, plus source fingerprint.
- `python test_guidelines_mcp_protocol.py`: a fresh stdio MCP handshake,
  advertised tool schema, two full specialist calls and legacy
  `read_guideline` call. Requires the existing documented
  `mcp[cli]>=2,<3` dependency. GitHub Actions runs both tests.
- The workflow verifies **repository-side fresh-client behavior only**.
  It cannot prove that a particular Codex/Claude installation picked up
  a new tool definition. Record that separately under Issue #32 A5.

Stop after a successful, actual external-client full-text read and directly
affected status reconciliation; do not manufacture a second product refactor.
