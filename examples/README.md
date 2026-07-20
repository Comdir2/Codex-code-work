# Code Work prompt examples

These examples describe realistic requests and the workflow the skill should encourage. They are not benchmark results and do not guarantee a particular implementation, duration, or test outcome. Repository instructions and the user's explicit decisions remain authoritative.

## 1. Root-cause defect fix

```text
Use $code-work to fix duplicate webhook deliveries being persisted when the
provider retries the same event ID. Keep the existing HTTP response contract
and database schema. First reproduce the issue, add a regression test at the
lowest reliable level, make the smallest root-cause fix, and run the affected
integration tests. Do not deploy or clean up historical rows.
```

Expected workflow:

- trace the event ID from the request boundary to persistence;
- distinguish an idempotency defect from test or retry behavior;
- demonstrate a focused failing case when practical;
- change only the responsible mechanism;
- verify the reproduction, adjacent delivery behavior, and the unchanged response contract;
- report that historical cleanup and deployment were intentionally not performed.

## 2. Bounded feature slice

```text
Use $code-work to add CSV export to the existing reports endpoint. The first
release must support the same filters as JSON, use UTF-8 with a header row,
and leave authentication and pagination unchanged. Implement one end-to-end
path, add contract coverage, run the reports tests, and do not add scheduled
exports or a UI.
```

Expected workflow:

- identify the endpoint's stable request and authorization seams;
- define an acceptance example for headers, encoding, filtering, and empty data;
- implement a thin path through real application behavior;
- exercise the public contract and relevant failure paths;
- leave scheduling and UI work outside the patch.

## 3. Behavior-preserving refactor

```text
Use $code-work to extract invoice total calculation from the controller into
the billing domain module. Preserve rounding, error messages, public APIs, and
serialized output exactly. Characterize the current boundary cases before the
refactor and run the billing and controller suites afterward.
```

Expected workflow:

- establish current observable behavior with existing or characterization tests;
- move one structural boundary without changing intended results;
- avoid opportunistic renaming or neighboring cleanup;
- compare behavior at the public seam and run relevant static checks.

## 4. Backward-compatible migration

```text
Use $code-work to introduce a nullable orders.external_reference column and
start writing it for new provider orders. Existing readers and old rows must
continue to work. Map producers and consumers, include the repository's normal
rollback mechanism, test old and new records, and do not backfill production.
```

Expected workflow:

- map schema ownership, writers, readers, and compatibility order;
- use a backward-compatible transition rather than assuming an atomic rollout;
- test old rows, new rows, and rollback behavior in the available test environment;
- classify production backfill and deployment as not performed.

## 5. Safe adaptive parallelism

```text
Use $code-work to add the same settled validation rule to the independent
Python and TypeScript SDK packages. Their public error code must be
INVALID_REGION. If isolated workers are available, inspect and test the two
packages in parallel with one writer per package; otherwise work sequentially.
Reconcile the combined diff and run the repository's cross-SDK contract check.
```

Expected workflow:

- settle the shared validation contract before parallel edits begin;
- give each package an exclusive write owner and independent test resources;
- reduce worker count or serialize if a shared fixture, lockfile, or generator is discovered;
- inspect and verify the integrated state after both slices are complete.

## 6. Shared-state task that should remain sequential

```text
Use $code-work to repair the migration ordering failure in the single test
database. Keep one executor for all schema and database operations, reproduce
the first failing migration, fix only the ordering mechanism, and rehearse the
repository's documented upgrade and rollback checks.
```

Expected workflow:

- serialize investigation and writes because all steps share one database and schema history;
- test a falsifiable root-cause hypothesis before editing;
- avoid using more workers merely because they are available;
- report any unavailable rollback environment as partial rather than confirmed evidence.

## 7. Implementation followed by independent verification

Implementation request:

```text
Use $code-work to implement the approved rate-limit headers without changing
the rate-limit algorithm. Add focused API contract tests and stop after the
local implementation and checks; do not commit or publish.
```

Separate verification request:

```text
Use $code-verification to review the resulting diff against the approved
header contract. Keep the review read-only, derive expected values from the
contract, rerun relevant tests, and identify any coverage or compatibility gap.
```

Expected workflow:

- Code Work owns the authorized implementation and its immediate evidence;
- [Code Verification](https://github.com/Comdir2/Codex-code-verification) independently evaluates the integrated result;
- any requested fix begins only after separate authorization.
