# Meta Data

Prefix: `/transaction-types`, `/property-types`, `/tags`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Transaction Types

### GET /transaction-types

Desc: View all transaction types.

**Access:** Requires sign-in
**Response:** `[TransactionTypeInfo]`

### POST /transaction-types

Desc: Create a transaction type.

**Access:** Admin only

**Rules:**
- If no ID is provided, one is automatically generated from the display name.
- Duplicate IDs are not allowed.
- ID format: lowercase letters, numbers, and underscores only (e.g., `ban`, `cho_thue`).

**Request:** `CreateTransactionTypeRequest`
**Response:** `TransactionTypeInfo` (201)

### GET /transaction-types/{entity_id}

Desc: View a transaction type by ID.

**Access:** Requires sign-in
**Response:** `TransactionTypeInfo`

### PUT /transaction-types/{entity_id}

Desc: Update a transaction type.

**Access:** Admin only

**Rules:**
- The ID cannot be changed. Only the display name can be updated.

**Request:** `UpdateTransactionTypeRequest`
**Response:** `TransactionTypeInfo`

### DELETE /transaction-types/{entity_id}

Desc: Delete a transaction type.

**Access:** Admin only

**Rules:**
- There is no referential integrity check — transaction types can be deleted even if currently used by properties.
- User assignment links are automatically removed.

**Response:** 204 No Content

---

## Property Types

### GET /property-types

Desc: View all property types.

**Access:** Requires sign-in
**Response:** `[PropertyTypeInfo]`

### POST /property-types

Desc: Create a property type.

**Access:** Admin only

**Rules:**
- Same auto-generated ID and uniqueness rules as transaction types.
- ID format: lowercase letters, numbers, and underscores only.

**Request:** `CreatePropertyTypeRequest`
**Response:** `PropertyTypeInfo` (201)

### GET /property-types/{entity_id}

Desc: View a property type by ID.

**Access:** Requires sign-in
**Response:** `PropertyTypeInfo`

### PUT /property-types/{entity_id}

Desc: Update a property type.

**Access:** Admin only

**Request:** `UpdatePropertyTypeRequest`
**Response:** `PropertyTypeInfo`

### DELETE /property-types/{entity_id}

Desc: Delete a property type.

**Access:** Admin only

**Rules:**
- There is no referential integrity check — property types can be deleted even if currently used by properties.
- User assignment links are automatically removed.

**Response:** 204 No Content

---

## Tags

### GET /tags

Desc: View all tags.

**Access:** Requires sign-in
**Response:** `[TagInfo]`

### POST /tags

Desc: Create a tag.

**Access:** Admin only

**Rules:**
- If no ID is provided, one is automatically generated from the display name.
- ID generation: converts to ASCII, lowercases, strips whitespace, replaces non-alphanumeric characters with hyphens, and removes leading/trailing hyphens.
- Duplicate IDs are not allowed.
- The ID is the primary identifier and cannot be changed after creation.
- ID format: lowercase letters, numbers, and hyphens only (e.g., `ban`, `cho-thue`). Note: tags use hyphens while other types use underscores.

**Request:** `CreateTagRequest`
**Response:** `TagInfo` (201)

### GET /tags/{tag_id}

Desc: View a tag by ID.

**Access:** Requires sign-in
**Response:** `TagInfo`

### PUT /tags/{tag_id}

Desc: Update a tag.

**Access:** Admin only

**Rules:**
- Only the display name can be updated. The ID cannot be changed.

**Request:** `UpdateTagRequest`
**Response:** `TagInfo`

### DELETE /tags/{tag_id}

Desc: Delete a tag.

**Access:** Admin only

**Rules:**
- Tags can be deleted even if currently referenced by properties.
- Tag associations with properties are automatically removed on deletion.

**Response:** 204 No Content

---

## Related

- [Properties](./properties.md) — tags, transaction types, property types linked to properties
- [Users](./users.md) — transaction types and property types assigned to users
