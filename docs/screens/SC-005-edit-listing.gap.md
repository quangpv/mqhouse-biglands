# Gap Analysis: SC-005 Edit Listing

## Against: openapi.yaml

---

## Missing Fields

**Resolved**: `propertyType` added to `UpdateListingRequest` schema.

## Naming & Constraint Gaps

### 1. Transaction type lock status unclear
- **Screen**: "Transaction type (locked after submission?)" — marked with question mark, indicating uncertainty
- **API**: `UpdateListingRequest` does not exclude `transactionType` — it can be changed on any edit
- **Domain Model**: No rule explicitly locks transactionType after submission
- **Impact**: If screen expects it locked but API allows changes, data integrity or re-approval logic may be bypassed
- **Fix**: Either (a) document that transactionType is immutable after first submission (write-once), or (b) add `transactionType` to the re-approval trigger list (LST-I05)

## Missing States

### 1. Re-approval trigger not signaled in response
- **Screen**: No confirmation message shown when edit triggers re-approval
- **API**: `PUT /listings/{id}` returns HTTP 200 with the updated `Listing` — but if the listing was CON_HANG and price/area changed, status silently flips to PENDING_APPROVAL
- **Impact**: Client code can't distinguish between "updated in place" (DRAFT → DRAFT) and "re-approval triggered" (CON_HANG → PENDING_APPROVAL) without comparing old and new status
- **Fix**: Add a response field `statusChanged: boolean` or `requiresApproval: boolean` to the 200 response

### 2. Image change triggers re-approval (ES-002)
- **Screen**: Images are editable. BDD (US-002-edit-listing EC2) says removing primary image on CON_HANG triggers re-approval
- **API**: `DELETE /listings/{id}/images/{imageId}` returns 204 — no indication that the listing status changed
- **Impact**: Same as above — client doesn't know the listing needs re-approval
- **Fix**: Return the updated `Listing` status (or a flag) from image mutations when the listing is CON_HANG

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Pre-filled form fields | `GET /listings/{id}` → `Listing` fields map to form | ✓ |
| Save changes | `PUT /listings/{id}` (partial update) | ✓ |
| Add image | `POST /listings/{id}/images` | ✓ |
| Remove image | `DELETE /listings/{id}/images/{imageId}` | ✓ |
| Reorder images | `PUT /listings/{id}/images/reorder` | ✓ |
| Set primary | `PUT /listings/{listingId}/images/{imageId}/primary` | ✓ |
| Submit for approval (DRAFT) | `POST /listings/{id}/submit` | ✓ |
