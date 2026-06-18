# Test Plan: Listing Management

> **Epic**: Listing Management  
> **Stories**: US-001-create-listing, US-002-edit-listing, US-003-manage-listing-status  
> **Total BDD Scenarios**: 35  
> **Endpoints**: POST /listings, GET /listings, GET /listings/{id}, PUT /listings/{id}, DELETE /listings/{id}, POST /listings/{id}/submit, POST /listings/{id}/withdraw, POST /listings/{id}/images, DELETE /listings/{listingId}/images/{imageId}, PUT /listings/{id}/images/reorder, PUT /listings/{listingId}/images/{imageId}/primary

---

## 1. Unit Tests

| ID | Facade | What to Test | Mocked Deps | Assertions |
|----|--------|-------------|-------------|------------|
| UT-LM-01 | `create_listing` | Save as DRAFT | ListingRepo | status=DRAFT, code generated |
| UT-LM-02 | `create_listing` | Submit → PENDING_APPROVAL | ListingRepo, ListingImageRepo | status=PENDING_APPROVAL, notification enqueued |
| UT-LM-03 | `create_listing` | Auto-approve for Admin | ListingRepo, current_user(ADMIN) | status=CON_HANG, approved_at set |
| UT-LM-04 | `create_listing` | Deactivated agent blocked | ListingRepo, current_user(inactive) | Raises ForbiddenError |
| UT-LM-05 | `create_listing` | Product code format | ListingRepo | code matches YYMMDD+random pattern |
| UT-LM-06 | `update_listing` | DRAFT edit no re-approval | ListingRepo | status stays DRAFT |
| UT-LM-07 | `update_listing` | Key field change on CON_HANG → PENDING_APPROVAL | ListingRepo | status changes to PENDING_APPROVAL |
| UT-LM-08 | `update_listing` | Non-key field on CON_HANG stays CON_HANG | ListingRepo | status unchanged |
| UT-LM-09 | `update_listing` | Non-owner blocked | ListingRepo, current_user | Raises ForbiddenError |
| UT-LM-10 | `delete_listing` | DRAFT deletion | ListingRepo | Hard delete called |
| UT-LM-11 | `delete_listing` | Non-DRAFT blocked | ListingRepo | Raises ConflictError |
| UT-LM-12 | `submit_listing` | Missing images blocked | ListingImageRepo(count→0) | Raises BadRequestError |
| UT-LM-13 | `submit_listing` | Already submitted blocked | ListingRepo(status≠DRAFT) | Raises ConflictError |
| UT-LM-14 | `withdraw_listing` | CON_HANG → DRAFT | ListingRepo | status changes to DRAFT |
| UT-LM-15 | `list_listings` | Default filters | ListingRepo | status=CON_HANG,DA_COC (visible only) |
| UT-LM-16 | `list_listings` | Hot filter | ListingRepo, UserPinRepo | isHot=true filter applied |
| UT-LM-17 | `list_listings` | Pinned filter | UserPinRepo(current_user) | Filtered to user's pinned listing IDs |

**Mapper Tests:**

| ID | Mapper | Input | Assertions |
|----|--------|-------|------------|
| UT-LM-18 | `listing_to_response` | ListingEntity full | All fields mapped, images NOT included (detail only) |
| UT-LM-19 | `listing_to_detail_response` | ListingEntity + images + dealEvents | Includes images, dealEvents, isPinned |
| UT-LM-20 | `build_listing_entity` | CreateListingRequest | All required fields set, code generated |
| UT-LM-21 | `apply_listing_update` | UpdateListingRequest + existing | Only provided fields changed |
| UT-LM-22 | `detect_reapproval_fields` | Update dict on CON_HANG | True if price/area changed, False otherwise |

---

## 2. Integration Tests

| ID | Flow | Setup | Steps | Assertions |
|----|------|-------|-------|------------|
| IT-LM-01 | Create listing DRAFT → DB | Agent JWT | POST /listings {action:save} → SELECT | DRAFT in DB, code non-null, created_by correct |
| IT-LM-02 | Create listing SUBMIT → PENDING | Agent JWT, images pre-uploaded | POST /listings {action:submit} → verify | PENDING_APPROVAL, notification created |
| IT-LM-03 | Create listing SUBMIT → no images | Agent JWT, 0 images | POST /listings {action:submit} | 400 image required |
| IT-LM-04 | Create listing → Admin auto-approve | Admin JWT | POST /listings {action:submit} | CON_HANG, approved_by_id set |
| IT-LM-05 | Create listing → product code unique | 2 listings same day | POST /listings twice | Different codes |
| IT-LM-06 | Edit DRAFT listing | Agent JWT | PUT /listings/{id} | 200, status=DRAFT still |
| IT-LM-07 | Edit CON_HANG price → re-approval | Agent JWT, CON_HANG listing | PUT /listings/{id} {price: new} | 200, status=PENDING_APPROVAL |
| IT-LM-08 | Edit CON_HANG description → no re-approval | Agent JWT, CON_HANG listing | PUT /listings/{id} {description: new} | 200, status=CON_HANG |
| IT-LM-09 | Edit → non-owner | Agent B token, Agent A's listing | PUT /listings/{id} | 403 |
| IT-LM-10 | Edit → terminal status | Agent JWT, HET_HANG listing | PUT /listings/{id} | 403 |
| IT-LM-11 | Delete DRAFT listing | Agent JWT | DELETE /listings/{id} | 204, not in DB |
| IT-LM-12 | Delete CON_HANG listing | Agent JWT | DELETE /listings/{id} | 409 |
| IT-LM-13 | Submit DRAFT listing | Agent JWT, images exist | POST /listings/{id}/submit | 200, PENDING_APPROVAL |
| IT-LM-14 | Submit CON_HANG listing | Agent JWT | POST /listings/{id}/submit | 409 |
| IT-LM-15 | Withdraw CON_HANG listing | Agent JWT | POST /listings/{id}/withdraw | 200, DRAFT |
| IT-LM-16 | Withdraw DRAFT listing | Agent JWT | POST /listings/{id}/withdraw | 409 |

---

## 3. API Tests

| ID | BDD | Endpoint | Request | Expected Status | Expected Response |
|----|-----|----------|---------|-----------------|-------------------|
| AT-LM-01 | US-001 H1 | POST /listings | Full valid, action=save | 201 | DRAFT, code returned |
| AT-LM-02 | US-001 H2 | POST /listings | Full valid, action=submit | 201 | PENDING_APPROVAL |
| AT-LM-03 | US-001 H3 | POST /listings | All optional fields | 201 | Optional fields saved |
| AT-LM-04 | US-001 E1 | POST /listings | No price | 400 | VALIDATION_ERROR |
| AT-LM-05 | US-001 E2 | POST /listings | action=submit, 0 images | 400 | image required |
| AT-LM-06 | US-001 E3 | POST /listings | price="abc" | 400 | VALIDATION_ERROR |
| AT-LM-07 | US-001 E4 | POST /listings | No commission | 400 | VALIDATION_ERROR |
| AT-LM-08 | US-001 E5 | POST /listings | Wrong ward/district cascade | 400 | VALIDATION_ERROR |
| AT-LM-09 | US-001 S1 | POST /listings | No auth | 401 | UNAUTHORIZED |
| AT-LM-10 | US-001 S2 | POST /listings | Expired session | 401 | UNAUTHORIZED |
| AT-LM-11 | US-002 H1 | PUT /listings/{id} | DRAFT, edit description | 200 | DRAFT, description changed |
| AT-LM-12 | US-002 H2 | PUT /listings/{id} | CON_HANG, edit description | 200 | CON_HANG (no re-approval) |
| AT-LM-13 | US-002 H3 | PUT /listings/{id} | CON_HANG, change price | 200 | PENDING_APPROVAL |
| AT-LM-14 | US-002 H4 | PUT /listings/{id} | DRAFT, then submit | 200 | PENDING_APPROVAL after submit |
| AT-LM-15 | US-002 E1 | PUT /listings/{id} | Non-owner | 403 | FORBIDDEN |
| AT-LM-16 | US-002 E2 | PUT /listings/{id} | Terminal status | 403 | FORBIDDEN |
| AT-LM-17 | US-002 S1 | PUT /listings/{id} | Approver on agent's listing | 403 | FORBIDDEN |
| AT-LM-18 | US-003 H1 | DELETE /listings/{id} | DRAFT listing | 204 | — |
| AT-LM-19 | US-003 H2 | POST /listings/{id}/withdraw | CON_HANG listing | 200 | DRAFT |
| AT-LM-20 | US-003 E1 | DELETE /listings/{id} | CON_HANG listing | 409 | CONFLICT |
| AT-LM-21 | US-003 E2 | POST /listings/{id}/withdraw | DRAFT listing | 409 | CONFLICT |
| AT-LM-22 | US-003 S1 | DELETE /listings/{id} | Approver token | 403 | FORBIDDEN |
| AT-LM-23 | US-003 S2 | DELETE /listings/{id} | Other agent token | 403 | FORBIDDEN |

---

## 4. Security Tests

| ID | BDD | Scenario | Expected Status |
|----|-----|----------|-----------------|
| SC-LM-01 | US-001 S1 | Create listing without auth | 401 |
| SC-LM-02 | US-001 S2 | Create listing with expired session | 401 (form data preserved by FE) |
| SC-LM-03 | US-002 S1 | Approver edits agent's listing | 403 |
| SC-LM-04 | US-002 S2 | Agent non-owner direct URL access | 403 |
| SC-LM-05 | US-003 S1 | Approver deletes listing | 403 |
| SC-LM-06 | US-003 S2 | Other agent deletes listing | 403 |
| SC-LM-07 | — | SQL injection in search term | 200 (no extra data) |
| SC-LM-08 | — | Mass assignment on forbidden fields | 400 (isHot, hotOrder ignored/validated) |

---

## 5. Load Tests

| ID | Scenario | Concurrent Users | Target | Duration |
|----|----------|-----------------|--------|----------|
| LD-LM-01 | Create listings | 15 | 30 req/s, p95 < 800ms | 2 min |
| LD-LM-02 | Browse listings (paginated) | 30 | 200 req/s, p95 < 300ms | 2 min |
| LD-LM-03 | Search listings by keyword | 20 | 100 req/s, p95 < 500ms | 2 min |
| LD-LM-04 | Concurrent edits on same listing | 5 | No race conditions, last write wins | 30s |
