# Test Plan: Approval Workflow

> **Epic**: Approval Workflow  
> **Stories**: US-001-approve-listing-post, US-002-reject-listing-post, US-003-bulk-approve  
> **Total BDD Scenarios**: 27  
> **Endpoints**: GET /approvals/queues, GET /approvals/queues/{queueType}, GET /approvals/{id}, POST /approvals/{id}/approve, POST /approvals/{id}/reject, POST /approvals/bulk-approve

---

## 1. Unit Tests

| ID | Facade | What to Test | Mocked | Assertions |
|----|--------|-------------|--------|------------|
| UT-AW-01 | `list_queues` | Grouped counts per transaction type | ApprovalRepo | 3 transaction types × 5 approval types = 15 groups |
| UT-AW-02 | `list_queue_items` | Filter by queueType | ApprovalRepo | Only matching type returned |
| UT-AW-03 | `list_queue_items` | Filter by transactionType | ApprovalRepo | Only that transaction type |
| UT-AW-04 | `approve_item` | Status validation per type | ApprovalRepo, ListingRepo | Correct status transition (per APPENDIX) |
| UT-AW-05 | `approve_item` | Deposit approval status → DA_COC | ApprovalRepo, ListingRepo, DealEventRepo | listing.status=DA_COC |
| UT-AW-06 | `approve_item` | Listing post approval → CON_HANG | ApprovalRepo, ListingRepo | listing.status=CON_HANG |
| UT-AW-07 | `approve_item` | Cancellation approval → HUY_COC (relist) | ApprovalRepo, ListingRepo, DealEventRepo | listing.status=HUY_COC |
| UT-AW-08 | `approve_item` | Already processed guard | ApprovalRepo(get_for_update→already decided) | Raises ConflictError(ALREADY_PROCESSED) |
| UT-AW-09 | `approve_item` | Approver approves own listing blocked | ApprovalRepo, ListingRepo, current_user(is also creator) | Raises ForbiddenError |
| UT-AW-10 | `reject_item` | Reason required | RejectRequest(reason empty) | Raises BadRequestError |
| UT-AW-11 | `reject_item` | Listing post rejection → DRAFT | ApprovalRepo, ListingRepo | listing.status=DRAFT |
| UT-AW-12 | `reject_item` | Deposit rejection → CON_HANG | ApprovalRepo, ListingRepo | listing.status=CON_HANG |
| UT-AW-13 | `bulk_approve` | Empty id list | ids=[] | Raises BadRequestError |
| UT-AW-14 | `bulk_approve` | Mixed success/failure | 3 items: 2 succeed, 1 fails | Returns BulkApproveResponse with 2 succeeded, 1 failed |
| UT-AW-15 | `bulk_approve` | Only LISTING_POST type allowed | Non-LISTING_POST items | Raises BadRequestError |

---

## 2. Integration Tests

| ID | Flow | Setup | Steps | Assertions |
|----|------|-------|-------|------------|
| IT-AW-01 | List approval queues | 5 pending across 3 types | GET /approvals/queues | 15 queue entries with counts |
| IT-AW-02 | List queue items for listing-post BAN | 3 pending BAN listings | GET /approvals/queues/listing-post?transactionType=BAN | 3 items with listing details |
| IT-AW-03 | Approve listing post | PENDING_APPROVAL listing | POST /approvals/{id}/approve | 200, CON_HANG, notification |
| IT-AW-04 | Approve deposit | CON_HANG with pending deposit | POST /approvals/{id}/approve | 200, DA_COC |
| IT-AW-05 | Approve cancellation | DA_COC with pending cancellation | POST /approvals/{id}/approve | 200, HUY_COC |
| IT-AW-06 | Approve closure | DA_COC with pending closure | POST /approvals/{id}/approve | 200, DA_CHOT |
| IT-AW-07 | Approve sold-out | CON_HANG with pending SOLD_OUT | POST /approvals/{id}/approve | 200, HET_HANG |
| IT-AW-08 | Reject listing post | PENDING_APPROVAL | POST /approvals/{id}/reject with reason | 200, DRAFT, rejection reason saved |
| IT-AW-09 | Reject deposit | Pending deposit | POST /approvals/{id}/reject with reason | 200, CON_HANG remains |
| IT-AW-10 | Reject without reason | Any pending | POST /approvals/{id}/reject {} | 400 |
| IT-AW-11 | Double approve race | Two requests | Both POST /approvals/{id}/approve simultaneously | 200 + 409 |
| IT-AW-12 | Bulk approve 5 listings | 5 pending | POST /approvals/bulk-approve {ids: [...]} | 5 succeeded, all CON_HANG |
| IT-AW-13 | Bulk approve with 1 failure | 3 pending, 1 already processed | POST /approvals/bulk-approve | 2 succeeded, 1 failed |
| IT-AW-14 | Approver cannot approve own listing | Approver's own listing pending | POST /approvals/{id}/approve | 403 FORBIDDEN |
| IT-AW-15 | Agent views queue | Agent JWT | GET /approvals/queues | 403 FORBIDDEN |

---

## 3. API Tests

| ID | BDD | Endpoint | Request | Status | Expected |
|----|-----|----------|---------|--------|----------|
| AT-AW-01 | US-001 H1 | POST /approvals/{id}/approve | Listing post | 200 | CON_HANG, notification |
| AT-AW-02 | US-001 H2 | POST /approvals/{id}/approve | Deposit approval | 200 | DA_COC |
| AT-AW-03 | US-001 H3 | POST /approvals/{id}/approve | Cancellation approval | 200 | HUY_COC |
| AT-AW-04 | US-001 H4 | POST /approvals/{id}/approve | Sold-out approval | 200 | HET_HANG |
| AT-AW-05 | US-001 E1 | POST /approvals/{id}/approve | Missing data | 400 | VALIDATION_ERROR |
| AT-AW-06 | US-001 E2 | POST /approvals/{id}/approve | Already processed | 409 | ALREADY_PROCESSED |
| AT-AW-07 | US-001 E3 | POST /approvals/{id}/approve | Not pending anymore | 409 | ALREADY_PROCESSED |
| AT-AW-08 | US-001 S1 | GET /approvals/queues | Agent token | 403 | FORBIDDEN |
| AT-AW-09 | US-001 S2 | POST /approvals/{id}/approve | Own listing | 403 | FORBIDDEN |
| AT-AW-10 | US-001 S3 | POST /approvals/{id}/approve | No auth | 401 | UNAUTHORIZED |
| AT-AW-11 | US-002 H1 | POST /approvals/{id}/reject | With reason | 200 | DRAFT, notif with reason |
| AT-AW-12 | US-002 H2 | POST /approvals/{id}/reject | Deposit rejection | 200 | CON_HANG remains |
| AT-AW-13 | US-002 H3 | POST /approvals/{id}/reject | Cancellation rejection | 200 | DA_COC remains |
| AT-AW-14 | US-002 E1 | POST /approvals/{id}/reject | No reason | 400 | VALIDATION_ERROR |
| AT-AW-15 | US-002 E2 | POST /approvals/{id}/reject | Already approved | 409 | ALREADY_PROCESSED |
| AT-AW-16 | US-002 S1 | POST /approvals/{id}/reject | Agent token | 403 | FORBIDDEN |
| AT-AW-17 | US-002 S2 | POST /approvals/{id}/reject | Admin (should work) | 200 | Works like approver |
| AT-AW-18 | US-003 H1 | POST /approvals/bulk-approve | 2 ids | 200 | 2 succeeded |
| AT-AW-19 | US-003 H2 | POST /approvals/bulk-approve | Select all | 200 | All approved |
| AT-AW-20 | US-003 E1 | POST /approvals/bulk-approve | Empty ids | 400 | VALIDATION_ERROR |
| AT-AW-21 | US-003 E2 | POST /approvals/bulk-approve | Mixed | 200 | Partial success |
| AT-AW-22 | US-003 S1 | POST /approvals/bulk-approve | Agent token | 403 | FORBIDDEN |

---

## 4. Security Tests

| ID | BDD | Scenario | Expected Status |
|----|-----|----------|-----------------|
| SC-AW-01 | US-001 S1 | Agent views approval queues | 403 |
| SC-AW-02 | US-001 S2 | Approver approves own listing | 403 |
| SC-AW-03 | US-001 S3 | No auth on approve | 401 |
| SC-AW-04 | US-002 S1 | Agent rejects listing | 403 |
| SC-AW-05 | US-003 S1 | Agent bulk approves | 403 |
| SC-AW-06 | — | Race: two approvers approve same item | One gets 409 |
| SC-AW-07 | — | Malformed approval UUID | 404 or 400 |

---

## 5. Load Tests

| ID | Scenario | Concurrent Users | Target | Duration |
|----|----------|-----------------|--------|----------|
| LD-AW-01 | List queue items | 10 | 50 req/s, p95 < 300ms | 2 min |
| LD-AW-02 | Approve items (sequential) | 5 | 20 req/s, p95 < 500ms | 2 min |
| LD-AW-03 | Bulk approve | 5 (50 items each) | No partial success beyond expected | 2 min |
| LD-AW-04 | Concurrent approve same item | 10 | Exactly 1 success, 9 failures | 30s |
