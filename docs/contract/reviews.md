# Reviews

Prefix: `/properties/{property_id}/reviews`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Any signed-in user can create and view reviews.
- Users can leave multiple reviews on the same property (no one-review-per-author restriction).
- Only the review author or an Admin can delete a review.
- Reviews are automatically removed when the property is deleted.

---

## GET /properties/{property_id}/reviews

Desc: View reviews for a property.

**Access:** Requires sign-in

**Rules:**
- Returns an error if the property is not found.
- Ordered by most recent first.
- Paginated (page default 1, size default 20, max 100).

**Response:** `ReviewListResponse`

---

## GET /properties/{property_id}/reviews/{review_id}

Desc: View review details.

**Access:** Requires sign-in

**Rules:**
- Returns an error if the review is not found or if the review does not belong to the specified property.
- Accessing a review via the wrong property ID returns an error.

**Response:** `ReviewDetailResponse`

---

## POST /properties/{property_id}/reviews

Desc: Create a review for a property.

**Access:** Requires sign-in

**Rules:**
- The property must exist in the system.
- Users can leave multiple reviews on the same property.
- If image IDs are provided, only valid file IDs are linked (invalid IDs are silently skipped).
- Review content is required (no length restriction).

**Request:** `CreateReviewRequest`
**Response:** `ReviewDetailResponse` (201)

---

## DELETE /properties/{property_id}/reviews/{review_id}

Desc: Delete a review.

**Access:** Requires sign-in

**Rules:**
- Only the review author or an Admin can delete the review.
- Returns an error if the review is not found or if the review does not belong to the specified property.
- Linked images are automatically removed when the review is deleted.

**Response:** 204 No Content

---

## Related

- [Files](./files.md) — image upload for reviews
- [Properties](./properties.md) — reviews are per-property
