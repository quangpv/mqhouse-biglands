# Reviews

Prefix: `/properties/{property_id}/reviews`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Any authenticated user can create and view reviews
- Multiple reviews per author per property are allowed (no one-review-per-author constraint)
- Delete requires ownership or ADMIN role
- Reviews cascade-delete when property is deleted

---

## GET /properties/{property_id}/reviews

Desc: List reviews for a property.

**Access:** Authenticated

**Rules:**
- 404 if property not found
- Ordered by `created_at DESC`
- Paginated (page default 1, size default 20, max 100)

**Response:** `ReviewListResponse`

---

## GET /properties/{property_id}/reviews/{review_id}

Desc: Get review detail.

**Access:** Authenticated

**Rules:**
- 404 if review not found OR if `review.property_id != property_id`
- Accessing a review via wrong property_id returns 404

**Response:** `ReviewDetailResponse`

---

## POST /properties/{property_id}/reviews

Desc: Create review for a property.

**Access:** Authenticated

**Rules:**
- 404 if property not found
- Multiple reviews per author per property are allowed
- If `file_ids` provided, only valid file IDs are linked (invalid IDs silently skipped)
- `content` is required (no length constraint)

**Request:** `CreateReviewRequest`
**Response:** `ReviewDetailResponse` (201)

---

## DELETE /properties/{property_id}/reviews/{review_id}

Desc: Delete a review.

**Access:** Authenticated

**Rules:**
- Only review author or ADMIN can delete (403 otherwise)
- 404 if review not found or property_id mismatch
- Cascade: linked `ReviewFileEntity` rows deleted

**Response:** 204 No Content

---

## Related

- [Files](./files.md) — image upload for reviews
- [Properties](./properties.md) — reviews are per-property
