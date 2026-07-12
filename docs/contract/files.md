# Files

Prefix: `/files`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Any authenticated user can upload and view files
- Delete requires ownership or ADMIN role
- Files are soft-deleted (moved to trash), not hard-deleted
- All non-GIF images are optimized to WebP on upload

---

## POST /files

Desc: Upload files (multipart).

**Access:** Authenticated

**Rules:**
- At least 1 file required (400 otherwise)
- Max 10 files per request (400 otherwise)
- Only image files accepted: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
- SVG explicitly rejected (400)
- Each file max 10MB (configurable via `max_upload_size_mb`)
- Filenames sanitized (non-word chars → `_`)
- Invalid/corrupted images rejected (400)

**Optimization rules:**
- JPEG/PNG/WebP → converted to WebP, quality 85, `optimize=True`
- RGBA/CMYK → converted to RGB before encoding
- GIF → saved as GIF (no conversion)
- Large images (>1920px on any side, non-GIF) → resized via Lanczos, max 1920px, aspect ratio preserved
- Small images → dimensions preserved
- EXIF metadata stripped
- Mimetype set to `image/webp` (non-GIF) or `image/gif` (GIF) regardless of original

**Thumbnail generation (non-GIF only, async):**
- `320w`: max 320px, WebP quality 85
- `640w`: max 640px, WebP quality 85

**Storage:** `{user_id}/{file_uuid}.webp` (or `.gif`)
**Size recorded:** Post-optimization size

**Request:** Multipart `{ files: Part[], entity_type: EntityType | null }`
**Response:** `FileUploadResponse`

---

## GET /files/{file_id}

Desc: Get file metadata.

**Access:** Authenticated

**Rules:**
- 404 if not found
- Path resolved from `storage_key` or `path` field

**Response:** `FileInfoResponse`

---

## DELETE /files/{file_id}

Desc: Delete file (soft delete / trash).

**Access:** Authenticated

**Rules:**
- Only file owner or ADMIN can delete (403 otherwise)
- File moved to `trash/{user_id}/{file_uuid}.{ext}`
- Thumbnails also moved to trash
- `deleted_at` timestamp set
- `storage_key` updated to trash path

**Response:** 204 No Content

---

## Background Cleanup

Not an HTTP endpoint — runs as scheduled job.

**Rules:**
- Temp files (`temp/` prefix): deleted after 24 hours
- Trash files: hard-deleted from DB and storage after 30 days
- Orphaned user files (no DB record): deleted after 24-hour grace period
- Valid user files (with DB records) are never touched

---

## Related

- [Properties](./properties.md) — images linked to properties, file_ids in transitions
- [Reviews](./reviews.md) — images linked to reviews
- [Auth](./auth.md) — avatar upload
