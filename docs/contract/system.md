# System

Geography, Master Data, Supports, Backfills, WebSocket.

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Geography

### GET /geography/provinces

Desc: List provinces.

**Access:** Public (no auth required)

**Rules:**
- Data is **static** — loaded from JSON file (`ho-chi-minh.json`), cached in memory
- Returns all provinces with nested districts and wards
- Province/district not found → returns empty list (no error)

**Response:** `[Province]`

### GET /geography/provinces/{province_id}/districts

Desc: List districts in a province.

**Access:** Public
**Response:** `[District]`

### GET /geography/provinces/{province_id}/districts/{district_id}/wards

Desc: List wards in a district.

**Access:** Public
**Response:** `[Ward]`

---

## Master Data

### GET /master-data

Desc: Get all enum values.

**Access:** Authenticated

**Rules:**
- No database call — returns Python enum values directly
- Includes: commission_types, direction_types, statuses, actions, notification_types, approval_statuses, user_roles, entity_types

**Response:** Master data object

---

## Supports

### GET /supports

Desc: Get support contact info.

**Access:** Authenticated

**Rules:**
- Returns first ADMIN user's `full_name` and `phone`
- Returns empty strings if no admins exist

**Response:** `{ admin_name: string, admin_phone: string | null }`

---

## Backfills

### POST /backfills

Desc: Rebuild search text index.

**Access:** ADMIN only

**Rules:**
- Loads all non-deleted properties with tags, property_type, transaction_type
- Computes `search_text` for each property
- Updates only if changed
- Returns `{ updated: int, total: int }`

**Response:** `{ updated: int, total: int }`

### GET /backfills

Desc: Check search index.

**Access:** ADMIN only

**Rules:**
- Normalizes search query (Vietnamese diacritics, abbreviations, number patterns)
- Performs property search using normalized query
- Computes `ts_rank` for each result
- Enriches with geography names, type names, tags

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

**Access:** Authenticated (JWT in query param)

**Rules:**
- Token decoded from `?token=` query parameter
- If `sub` (user_id) missing from payload → closes with code 4001
- Multiple simultaneous connections per user supported
- Server only processes incoming text messages (keep-alive loop); no business logic from client messages
- Dead connections auto-cleaned on send failure

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
