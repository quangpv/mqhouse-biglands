# Test Plan: Shared Cart Browsing

> **Epic**: Shared Cart Browsing  
> **Stories**: US-001-browse-listings, US-002-search-listings, US-003-filter-listings, US-004-view-product-detail, US-005-pin-listings  
> **Total BDD Scenarios**: 37  
> **Endpoints**: GET /listings, GET /listings/{id}, PUT /listings/{id}/pin, DELETE /listings/{id}/pin, GET /users/me/pins, GET /hot-listings, GET /notifications/unread-count, GET /approvals/queues

---

## 1. Unit Tests

| ID | Facade | What to Test | Mocked Deps | Assertions |
|----|--------|-------------|-------------|------------|
| UT-SC-01 | `list_listings` | Default sort by createdAt desc | ListingRepo | sortBy=createdAt, sortOrder=desc |
| UT-SC-02 | `list_listings` | Pagination | ListingRepo | page, size passed through |
| UT-SC-03 | `list_listings` | Search term filtering | ListingRepo | q param passed to filter |
| UT-SC-04 | `list_listings` | Hot filter tab | ListingRepo | isHot=true filter applied |
| UT-SC-05 | `list_listings` | Pinned filter tab | UserPinRepo, ListingRepo | Pinned IDs retrieved, filtered |
| UT-SC-06 | `list_listings` | Transaction type filter | ListingRepo | transactionType filter applied |
| UT-SC-07 | `list_listings` | Status filter | ListingRepo | status filter applied |
| UT-SC-08 | `get_listing` | Includes isPinned flag | UserPinRepo | isPinned=true/false based on user |
| UT-SC-09 | `get_listing` | Includes images | ListingImageRepo | Image list sorted by order |
| UT-SC-10 | `get_listing` | Includes dealEvents | DealEventRepo | Events ordered by createdAt |
| UT-SC-11 | `pin_listing` | First pin creates | UserPinRepo | New UserPin record created |
| UT-SC-12 | `unpin_listing` | Existing pin removed | UserPinRepo | Record deleted |
| UT-SC-13 | `list_my_pins` | Returns user's pinned listings | UserPinRepo, ListingRepo | Only user's pins returned |

---

## 2. Integration Tests

| ID | Flow | Setup | Steps | Assertions |
|----|------|-------|-------|------------|
| IT-SC-01 | Browse all listings | Agent JWT, 5 listings in DB | GET /listings | 200, 5 items, pagination metadata |
| IT-SC-02 | Browse with hot section | 3 hot + 10 normal listings | GET /listings?filter=hot | Hot listings first with isHot=true |
| IT-SC-03 | Browse empty state | Agent JWT, 0 listings | GET /listings | 200, empty data array, totalItems=0 |
| IT-SC-04 | Search by product code | Known code from setup | GET /listings?q=250520 | Matching listing returned |
| IT-SC-05 | Search by address keyword | Known address | GET /listings?q=Nguy%E1%BB%85n+Hu%E1%BB%87 | Matching listing returned |
| IT-SC-06 | Search with special chars | Search "<script>" | GET /listings?q=%3Cscript%3E | 200, no error, 0 results |
| IT-SC-07 | Filter by Hot tab | 2 hot listings | GET /listings?filter=hot | 2 hot listings returned |
| IT-SC-08 | Filter by Pinned tab | Agent pinned 3 listings | GET /listings?filter=pinned | 3 pinned listings |
| IT-SC-09 | Filter by All (default) | All active | GET /listings?filter=all | All CON_HANG + DA_COC |
| IT-SC-10 | View product detail | Listing with images + events | GET /listings/{id} | Full detail with images, events, isPinned |
| IT-SC-11 | View product detail → not found | Random UUID | GET /listings/{id} | 404 |
| IT-SC-12 | Pin a listing | Agent JWT | PUT /listings/{id}/pin | 200, UserPin created |
| IT-SC-13 | Unpin a listing | Already pinned | DELETE /listings/{id}/pin | 204 |
| IT-SC-14 | Pin same listing twice (toggle) | Already pinned | PUT /listings/{id}/pin | 200 (idempotent, no error) |
| IT-SC-15 | List my pins | 3 pinned listings | GET /users/me/pins | 3 listings returned |
| IT-SC-16 | Both users pin same listing | User A + User B pin same listing | Both pin | Independent pins per user |

---

## 3. API Tests

| ID | BDD | Endpoint | Request / Query | Expected Status | Expected Response |
|----|-----|----------|-----------------|-----------------|-------------------|
| AT-SC-01 | US-001 H1 | GET /listings | Default params | 200 | Grid, pagination, totalCount |
| AT-SC-02 | US-001 H2 | GET /listings | Approver JWT | 200 | Same view as agent |
| AT-SC-03 | US-001 H3 | GET /listings | Admin JWT | 200 | Same + sidebar counts |
| AT-SC-04 | US-001 H4 | GET /listings | `?page=2&size=5` | 200 | 5 items, page=2 |
| AT-SC-05 | US-001 H5 | GET /listings | `?filter=hot` | 200 | Hot items in response |
| AT-SC-06 | US-001 E1 | GET /listings | Empty DB | 200 | Empty data, totalItems=0 |
| AT-SC-07 | US-001 S1 | GET /listings | No auth | 401 | UNAUTHORIZED |
| AT-SC-08 | US-001 S2 | GET /api/vi/listings | No session | 401 | UNAUTHORIZED |
| AT-SC-09 | US-002 H1 | GET /listings | `?q=250520` | 200 | Matching by code |
| AT-SC-10 | US-002 H2 | GET /listings | `?q=CHDV+Qu%E1%BA%ADn+1` | 200 | Matches title |
| AT-SC-11 | US-002 H3 | GET /listings | `?q=Nguy%E1%BB%85n+Hu%E1%BB%87` | 200 | Matches address |
| AT-SC-12 | US-002 E1 | GET /listings | `?q=ZZZZNONEXISTENT` | 200 | Empty data |
| AT-SC-13 | US-002 E2 | GET /listings | `?q=%3Cscript%3E` | 200 | Safe, no error |
| AT-SC-14 | US-002 S1 | GET /listings | `?q=' OR 1=1 --` | 200 | No extra data leaked |
| AT-SC-15 | US-003 H1 | GET /listings | `?filter=hot` | 200 | Only hot items |
| AT-SC-16 | US-003 H2 | GET /listings | `?filter=pinned` | 200 | Only this agent's pins |
| AT-SC-17 | US-003 H3 | GET /listings | `?filter=all` | 200 | All active listings |
| AT-SC-18 | US-003 E1 | GET /listings | `?filter=pinned`, 0 pins | 200 | Empty data |
| AT-SC-19 | US-003 E2 | GET /listings | `?filter=hot`, 0 hot | 200 | Empty data |
| AT-SC-20 | US-003 EC1 | GET /listings | `?filter=pinned&q=...` | 200 | Scoped within pins |
| AT-SC-21 | US-004 H1 | GET /listings/{id} | Agent JWT | 200 | Full detail |
| AT-SC-22 | US-004 H2 | GET /listings/{id} | Owner JWT | 200 | Edit button data (ownership) |
| AT-SC-23 | US-004 H3 | GET /listings/{id} | Non-owner | 200 | No edit data |
| AT-SC-24 | US-004 H4 | GET /listings/{id} | DA_COC listing | 200 | Context-dependent buttons |
| AT-SC-25 | US-004 E1 | GET /listings/{id} | Non-existent ID | 404 | NOT_FOUND |
| AT-SC-26 | US-004 S1 | GET /listings/{id} | No auth | 401 | UNAUTHORIZED |
| AT-SC-27 | US-005 H1 | PUT /listings/{id}/pin | Not pinned | 200 | Pinned |
| AT-SC-28 | US-005 H2 | PUT /listings/{id}/pin | Already pinned (toggle) | 200 | Unpinned |
| AT-SC-29 | US-005 H3 | GET /listings | `?filter=pinned` after pin | 200 | Listing appears |
| AT-SC-30 | US-005 S1 | PUT /listings/{id}/pin | No auth | 401 | UNAUTHORIZED |

---

## 4. Security Tests

| ID | BDD | Scenario | Expected Status |
|----|-----|----------|-----------------|
| SC-SC-01 | US-001 S1 | Browse without auth | 401 |
| SC-SC-02 | US-001 S2 | Direct API access without session | 401 |
| SC-SC-03 | US-002 S1 | SQLi in search | 200 (no leak) |
| SC-SC-04 | US-002 S2 | XSS in search | 200 (sanitized) |
| SC-SC-05 | US-003 S1 | Filter without auth | 401 |
| SC-SC-06 | US-004 S1 | Detail without auth | 401 |
| SC-SC-07 | US-005 S1 | Pin without auth | 401 |
| SC-SC-08 | — | IDOR: view listing owned by another org | 200 (browse is public-within-auth) |

---

## 5. Load Tests

| ID | Scenario | Concurrent Users | Target | Duration |
|----|----------|-----------------|--------|----------|
| LD-SC-01 | Browse homepage | 50 | 500 req/s, p95 < 300ms | 3 min |
| LD-SC-02 | Search | 30 | 200 req/s, p95 < 500ms | 2 min |
| LD-SC-03 | View product detail | 40 | 200 req/s, p95 < 300ms | 2 min |
| LD-SC-04 | Pin/unpin toggle storm | 20 | No duplicate pins or data loss | 30s |
