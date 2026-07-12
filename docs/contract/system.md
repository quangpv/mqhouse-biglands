# System

Geography, Master Data, Supports, Backfills, WebSocket.

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Geography

### GET /geography/provinces

Desc: View all provinces.

**Access:** Public (no sign-in required)

**Rules:**
- Geography data is fixed and pre-loaded (not editable through the system).
- Returns all provinces with nested districts and wards.
- If a province or district is not found, an empty list is returned (no error).

**Response:** `[Province]`

### GET /geography/provinces/{province_id}/districts

Desc: View districts in a province.

**Access:** Public
**Response:** `[District]`

### GET /geography/provinces/{province_id}/districts/{district_id}/wards

Desc: View wards in a district.

**Access:** Public
**Response:** `[Ward]`

---

## Master Data

### GET /master-data

Desc: View all system-wide option values.

**Access:** Requires sign-in

**Rules:**
- Returns all available options without hitting the database.
- Includes: commission types, direction types, statuses, actions, notification types, approval statuses, user roles, entity types.

**Response:** Master data object

---

## Supports

### GET /supports

Desc: View support contact information.

**Access:** Requires sign-in

**Rules:**
- Returns the name and phone number of the first Admin user.
- Returns empty values if no Admin accounts exist.

**Response:** `{ admin_name: string, admin_phone: string | null }`

---

## Backfills

### POST /backfills

Desc: Rebuild the search index.

**Access:** Admin only

**Rules:**
- Loads all active properties with their tags, property types, and transaction types.
- Recalculates the search text for each property.
- Updates only properties where the search text has changed.
- Returns the number of updated properties and the total number of properties processed.

**Response:** `{ updated: int, total: int }`

### GET /backfills

Desc: Test the search index with a sample query.

**Access:** Admin only

**Rules:**
- Normalizes the search query (Vietnamese diacritics, abbreviations, number patterns).
- Performs a property search using the normalized query.
- Ranks each result by relevance.
- Enriches results with geography names, type names, and tags.

**Search normalization:**
- Vietnamese diacritics → ASCII (unidecode)
- Abbreviation expansion: q1→quan 1, chdv→can ho dich vu, mt→mat tien, cc→chung cu, hcm→ho chi minh, nb→nha ban, nt→noi that, vp→van phong, lh→lien he, ht→ho tro
- Number patterns: 2tr→2 trieu, 3ty→3 ty
- Whitespace collapse

**Query Params:** `search` (required), `page` (default 1), `size` (default 10, max 100)
**Response:** Search results with highlights

---

## WebSocket

### Connection: `ws://host/ws?token={jwt_token}`

**Access:** Requires sign-in (token passed in query string)

**Rules:**
- Token is decoded from the `?token=` query parameter.
- If the user ID is missing from the token, the connection is closed.
- Multiple simultaneous connections per user are supported.
- The server only processes incoming text messages (keep-alive loop); no business logic is triggered by client messages.
- Dead connections are automatically cleaned up on send failure.

**Outbound Events:**
```json
{
  "type": "notification_created",
  "event_type": "listing_post_created",
  "reference_type": "property",
  "reference_id": "uuid"
}
```

**Error Events:**
```json
{
  "type": "error",
  "data": { "message": "string" }
}
```

---

## Related

- [Notifications](./notifications.md) — WebSocket delivers notification events
- [Properties](./properties.md) — geography used in property search, search text backfill
