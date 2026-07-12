# Files

Prefix: `/files`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix.

---

## Global Rules

- Any signed-in user can upload and view files.
- Only the person who uploaded a file or an Admin can remove it.
- Files are soft-deleted (moved to trash), not permanently deleted immediately.
- All non-GIF images are automatically optimized to WebP format on upload.

---

## POST /files

Desc: Upload files.

**Access:** Requires sign-in

**Rules:**
- Must upload at least one file.
- Maximum of 10 files per upload.
- Only image files are accepted: JPEG, PNG, WebP, GIF.
- SVG files are not supported.
- Each file must be under 10MB (configurable via `max_upload_size_mb`).
- Filenames are sanitized (non-word characters replaced with `_`).
- Invalid or corrupted images are rejected.

**Optimization rules:**
- JPEG/PNG/WebP → converted to WebP, quality 85, optimized for size.
- RGBA/CMYK images → converted to RGB before encoding.
- GIF → saved as GIF (no conversion).
- Large images (longer than 1920px on any side, non-GIF) → resized to max 1920px, aspect ratio preserved.
- Small images → dimensions preserved.
- EXIF metadata is removed.
- Mimetype is set to `image/webp` (non-GIF) or `image/gif` (GIF) regardless of original format.

**Thumbnail generation (non-GIF only, generated asynchronously):**
- `320w`: max 320px wide, WebP quality 85
- `640w`: max 640px wide, WebP quality 85

**Storage:** `{user_id}/{file_uuid}.webp` (or `.gif`)
**Size recorded:** Post-optimization size
**Content hash:** SHA-256 hash computed and stored for each file for deduplication and integrity verification

**Request:** Multipart `{ files: Part[], entity_type: EntityType | null }`
**Response:** `FileUploadResponse`

---

## GET /files/{file_id}

Desc: View file metadata.

**Access:** Requires sign-in

**Rules:**
- Returns an error if the file is not found.
- File location is resolved from the storage key or path.

**Response:** `FileInfoResponse`

---

## DELETE /files/{file_id}

Desc: Delete a file (move to trash).

**Access:** Requires sign-in

**Rules:**
- Only the file owner or an Admin can delete the file.
- File is moved to a trash folder.
- Thumbnails are also moved to trash.
- A deletion timestamp is recorded.
- The storage location is updated to the trash path.

**Response:** 204 No Content

---

## Background Cleanup

Not an HTTP endpoint — runs as a scheduled job.

**Rules:**
- Temporary files (uploaded to `temp/` folder): deleted after 24 hours.
- Trash files: permanently deleted from the database and storage after 30 days.
- Orphaned files (files without a database record): deleted after a 24-hour grace period.
- Valid files (with database records) are never touched by cleanup.

---

## Related

- [Properties](./properties.md) — images linked to properties, file IDs in transitions
- [Reviews](./reviews.md) — images linked to reviews
- [Auth](./auth.md) — avatar upload
