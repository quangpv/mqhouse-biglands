# Meta Data

Prefix: `/transaction-types`, `/property-types`, `/tags`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Transaction Types

### GET /transaction-types

Desc: List all transaction types.

**Access:** Authenticated
**Response:** `[TransactionTypeInfo]`

### POST /transaction-types

Desc: Create transaction type.

**Access:** ADMIN only

**Rules:**
- If `id` is empty/None, auto-generates slug from `display_name`
- Uniqueness checked on ID (409 if duplicate)

**Request:** `CreateTransactionTypeRequest`
**Response:** `TransactionTypeInfo` (201)

### GET /transaction-types/{entity_id}

Desc: Get transaction type by ID.

**Access:** Authenticated
**Response:** `TransactionTypeInfo`

### PUT /transaction-types/{entity_id}

Desc: Update transaction type.

**Access:** ADMIN only

**Rules:**
- ID is immutable; only `display_name` updated

**Request:** `UpdateTransactionTypeRequest`
**Response:** `TransactionTypeInfo`

### DELETE /transaction-types/{entity_id}

Desc: Delete transaction type.

**Access:** ADMIN only

**Rules:**
- DB FK constraint may prevent deletion if in use by properties
- User assignment links cascade-delete

**Response:** 204 No Content

---

## Property Types

### GET /property-types

Desc: List all property types.

**Access:** Authenticated
**Response:** `[PropertyTypeInfo]`

### POST /property-types

Desc: Create property type.

**Access:** ADMIN only

**Rules:**
- Same slug auto-generation and uniqueness as transaction types

**Request:** `CreatePropertyTypeRequest`
**Response:** `PropertyTypeInfo` (201)

### GET /property-types/{entity_id}

Desc: Get property type by ID.

**Access:** Authenticated
**Response:** `PropertyTypeInfo`

### PUT /property-types/{entity_id}

Desc: Update property type.

**Access:** ADMIN only

**Request:** `UpdatePropertyTypeRequest`
**Response:** `PropertyTypeInfo`

### DELETE /property-types/{entity_id}

Desc: Delete property type.

**Access:** ADMIN only

**Rules:**
- Same cascade behavior as transaction types

**Response:** 204 No Content

---

## Tags

### GET /tags

Desc: List all tags.

**Access:** Authenticated
**Response:** `[TagInfo]`

### POST /tags

Desc: Create tag.

**Access:** ADMIN only

**Rules:**
- If `id` is None/empty/whitespace, auto-generates slug from `display_name`
- Slug algorithm: unidecode → lowercase → strip whitespace → replace non-alphanumeric with hyphens → strip leading/trailing hyphens
- Uniqueness checked on ID (409 if duplicate)
- ID is the primary key (String(50)), immutable after creation

**Request:** `CreateTagRequest`
**Response:** `TagInfo` (201)

### GET /tags/{tag_id}

Desc: Get tag by ID.

**Access:** Authenticated
**Response:** `TagInfo`

### PUT /tags/{tag_id}

Desc: Update tag.

**Access:** ADMIN only

**Rules:**
- Only `display_name` updated; ID immutable

**Request:** `UpdateTagRequest`
**Response:** `TagInfo`

### DELETE /tags/{tag_id}

Desc: Delete tag.

**Access:** ADMIN only

**Rules:**
- DB FK from `property_tags` handles referential integrity

**Response:** 204 No Content

---

## Related

- [Properties](./properties.md) — tags, transaction types, property types linked to properties
- [Users](./users.md) — transaction_type_ids and property_type_ids assigned to users
