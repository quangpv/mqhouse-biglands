# Test Plan: Deposit & Deal Lifecycle

> **Epic**: Deposit/Deal Lifecycle  
> **Stories**: US-001-report-deposit, US-002-approve-deposit, US-003-report-deal-closure, US-004-report-cancellation, US-005-approve-cancellation, US-006-mark-sold-out  
> **Total BDD Scenarios**: 60  
> **Endpoints**: POST /listings/{id}/deal-events/deposit, POST /listings/{id}/deal-events/closure, POST /listings/{id}/deal-events/cancellation, POST /listings/{id}/deal-events/sold-out

---

## 1. Unit Tests

| ID | Facade | What to Test | Mocked | Assertions |
|----|--------|-------------|--------|------------|
| UT-DL-01 | `report_deposit` | Valid report on CON_HANG | ListingRepo, DealEventRepo | DEPOSIT_REPORTED created, listing stays CON_HANG |
| UT-DL-02 | `report_deposit` | Duplicate pending deposit blocked | DealEventRepo(has_active_deposit→True) | Raises ConflictError(DUPLICATE_DEPOSIT) |
| UT-DL-03 | `report_deposit` | Missing customerName | Validation | Raises BadRequestError |
| UT-DL-04 | `report_deposit` | depositAmount ≤ 0 | Validation | Raises BadRequestError |
| UT-DL-05 | `report_deposit` | Non-CON_HANG listing | ListingRepo(status≠CON_HANG) | Raises ConflictError(INVALID_STATUS_TRANSITION) |
| UT-DL-06 | `report_closure` | Valid on DA_COC | DealEventRepo (deposit confirmed) | CLOSURE_REPORTED created |
| UT-DL-07 | `report_closure` | No active deposit | DealEventRepo (no confirmed deposit) | Raises ConflictError |
| UT-DL-08 | `report_closure` | Duplicate pending closure | DealEventRepo (pending closure exists) | Raises ConflictError |
| UT-DL-09 | `report_cancellation` | Requires notes | Validation (empty notes) | Raises BadRequestError |
| UT-DL-10 | `report_cancellation` | Valid on DA_COC | ListingRepo, DealEventRepo | CANCELLATION_REPORTED created |
| UT-DL-11 | `report_sold_out` | Valid on CON_HANG | ListingRepo | SOLD_OUT_REPORTED created |
| UT-DL-12 | `report_sold_out` | Duplicate pending | DealEventRepo | Raises ConflictError |
| UT-DL-13 | `report_sold_out` | Not on DA_COC | ListingRepo(status=DA_COC) | Raises ConflictError |
| UT-DL-14 | DealEventRepo | `has_active_deposit()` | — | True if DEPOSIT_REPORTED without DEPOSIT_CONFIRMED or CANCELLATION_CONFIRMED |

---

## 2. Integration Tests

| ID | Flow | Setup | Steps | Assertions |
|----|------|-------|-------|------------|
| IT-DL-01 | Full deposit flow | CON_HANG listing | report deposit → approve deposit → verify | DA_COC status, DealEvent confirmed |
| IT-DL-02 | Full closure flow | DA_COC listing | report closure → approve closure → verify | DA_CHOT status, terminal |
| IT-DL-03 | Full cancellation flow | DA_COC listing | report cancellation → approve cancellation → verify | HUY_COC status, listing relisted |
| IT-DL-04 | Full sold-out flow | CON_HANG listing | report sold-out → approve → verify | HET_HANG status, terminal |
| IT-DL-05 | Deposit rejected | CON_HANG listing | report deposit → reject → verify | CON_HANG remains, rejection recorded |
| IT-DL-06 | Cancellation rejected | DA_COC listing | report cancellation → reject → verify | DA_COC remains |
| IT-DL-07 | Double deposit on same listing | CON_HANG | report deposit twice | Second rejected, DUPLICATE_DEPOSIT |
| IT-DL-08 | Closure on non-deposited listing | CON_HANG (no deposit) | report closure | 409 rejected |
| IT-DL-09 | Closure on already-sold listing | HET_HANG | report closure | 409 rejected |
| IT-DL-10 | Approver rejects deposit | Pending deposit | POST /approvals/{id}/reject | 200, listing stays CON_HANG |
| IT-DL-11 | Approver double-approves | Already approved | POST /approvals/{id}/approve | 409 ALREADY_PROCESSED |
| IT-DL-12 | Approver rejects cancellation | Pending cancellation | POST /approvals/{id}/reject with reason | 200, listing stays DA_COC |

---

## 3. API Tests

| ID | BDD | Endpoint | Request | Status | Expected |
|----|-----|----------|---------|--------|----------|
| AT-DL-01 | US-001 H1 | POST .../deposit | `{customerName, depositAmount}` | 201 | DealEvent created |
| AT-DL-02 | US-001 H2 | POST .../deposit | With customerPhone | 201 | Phone saved |
| AT-DL-03 | US-001 H3 | POST .../deposit | With notes | 201 | Notes saved |
| AT-DL-04 | US-001 E1 | POST .../deposit | No customerName | 400 | VALIDATION_ERROR |
| AT-DL-05 | US-001 E2 | POST .../deposit | customerName too short (< 2) | 400 | VALIDATION_ERROR |
| AT-DL-06 | US-001 E3 | POST .../deposit | depositAmount = 0 | 400 | VALIDATION_ERROR |
| AT-DL-07 | US-001 E4 | POST .../deposit | No depositAmount | 400 | VALIDATION_ERROR |
| AT-DL-08 | US-001 E5 | POST .../deposit | Duplicate deposit on listing | 409 | DUPLICATE_DEPOSIT |
| AT-DL-09 | US-001 S1 | POST .../deposit | No auth | 401 | UNAUTHORIZED |
| AT-DL-10 | US-001 S2 | POST .../deposit | Inactive user | 403 | FORBIDDEN |
| AT-DL-11 | US-002 H1 | POST /approvals/{id}/approve | Deposit approval | 200 | DA_COC, notification sent |
| AT-DL-12 | US-002 H2 | POST /approvals/{id}/approve | Deposit with customerName, amount | 200 | Events confirmed |
| AT-DL-13 | US-002 H3 | POST /approvals/{id}/approve | Notify agent | 200 | Notification created |
| AT-DL-14 | US-002 E1 | POST /approvals/{id}/reject | No reason | 400 | VALIDATION_ERROR |
| AT-DL-15 | US-002 S1 | POST /approvals/{id}/approve | Agent token | 403 | FORBIDDEN |
| AT-DL-16 | US-003 H1 | POST .../closure | DA_COC listing | 201 | CLOSURE_REPORTED |
| AT-DL-17 | US-003 H2 | POST .../closure | With notes | 201 | Notes saved |
| AT-DL-18 | US-003 E1 | POST .../closure | CON_HANG listing (no deposit) | 409 | CONFLICT |
| AT-DL-19 | US-003 E2 | POST .../closure | Duplicate | 409 | CONFLICT |
| AT-DL-20 | US-003 S1 | POST .../closure | No auth | 401 | UNAUTHORIZED |
| AT-DL-21 | US-004 H1 | POST .../cancellation | DA_COC listing, with notes | 201 | CANCELLATION_REPORTED |
| AT-DL-22 | US-004 E1 | POST .../cancellation | No notes | 400 | VALIDATION_ERROR |
| AT-DL-23 | US-004 E2 | POST .../cancellation | CON_HANG listing | 409 | CONFLICT |
| AT-DL-24 | US-004 E3 | POST .../cancellation | Duplicate pending | 409 | CONFLICT |
| AT-DL-25 | US-004 S1 | POST .../cancellation | No auth | 401 | UNAUTHORIZED |
| AT-DL-26 | US-005 H1 | POST /approvals/{id}/approve | Cancellation approval | 200 | HUY_COC, relisted |
| AT-DL-27 | US-005 H2 | POST /approvals/{id}/reject | Cancellation with reason | 200 | DA_COC remains |
| AT-DL-28 | US-005 H3 | POST /approvals/{id}/approve | Admin approves cancellation | 200 | HUY_COC |
| AT-DL-29 | US-005 E1 | POST /approvals/{id}/reject | No reason | 400 | VALIDATION_ERROR |
| AT-DL-30 | US-005 S1 | POST /approvals/{id}/approve | Agent token | 403 | FORBIDDEN |
| AT-DL-31 | US-006 H1 | POST .../sold-out | CON_HANG listing | 201 | SOLD_OUT_REPORTED |
| AT-DL-32 | US-006 H2 | POST .../sold-out | Seller is not owner | 201 | Any agent can report |
| AT-DL-33 | US-006 H3 | POST .../sold-out | With notes | 201 | Notes saved |
| AT-DL-34 | US-006 E1 | POST .../sold-out | DA_COC listing | 409 | CONFLICT |
| AT-DL-35 | US-006 E2 | POST .../sold-out | Duplicate pending | 409 | CONFLICT |
| AT-DL-36 | US-006 S1 | POST .../sold-out | No auth | 401 | UNAUTHORIZED |

---

## 4. Security Tests

| ID | BDD | Scenario | Expected Status |
|----|-----|----------|-----------------|
| SC-DL-01 | US-001 S1 | Report deposit without auth | 401 |
| SC-DL-02 | US-001 S2 | Report deposit with inactive account | 403 |
| SC-DL-03 | US-001 S3 | Approver reports deposit (role OK) | 201 |
| SC-DL-04 | US-002 S1 | Agent approves deposit | 403 |
| SC-DL-05 | US-002 S2 | Non-approver accesses approval endpoint | 403 |
| SC-DL-06 | US-003 S1 | Report closure without auth | 401 |
| SC-DL-07 | US-004 S1 | Report cancellation without auth | 401 |
| SC-DL-08 | US-005 S1 | Agent approves cancellation | 403 |
| SC-DL-09 | US-006 S1 | Report sold-out without auth | 401 |
| SC-DL-10 | — | Race condition: two approvers approve same deposit simultaneously | One succeeds, one gets 409 |
| SC-DL-11 | — | Concurrent deposit report + approval collision | No illegal state (e.g., double DA_COC) |

---

## 5. Load Tests

| ID | Scenario | Concurrent Users | Target | Duration |
|----|----------|-----------------|--------|----------|
| LD-DL-01 | Report deposit | 10 | 30 req/s, p95 < 500ms | 2 min |
| LD-DL-02 | Approve deposit (sequential) | 5 | 10 req/s, p95 < 500ms | 2 min |
| LD-DL-03 | Concurrent approval race | 5 on same item | Exactly 1 succeeds | 30s |
| LD-DL-04 | Full lifecycle (deposit→closure→approve) | 10 pipelines | No inconsistent states | 2 min |
