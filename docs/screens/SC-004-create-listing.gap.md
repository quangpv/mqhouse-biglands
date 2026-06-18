# Gap Analysis: SC-004 Create Listing

## Against: openapi.yaml

---

## Missing Fields

### 1. `propertyType` (Loại) — Resolved
- **Screen**: Combobox field "Loại (*)" (Property Type) marked as required
- **Fix Applied**: `PropertyType` enum added to openapi.yaml with 10 values (`NHA_PHO`, `CAN_HO`, `CHDV`, `DAT`, `BIET_THU`, `VAN_PHONG`, `MAT_BANG`, `KHO_XUONG`, `NHA_TRO`, `KHAC`). Added to `Listing`, `CreateListingRequest`, and `UpdateListingRequest` schemas. Added to Listing entity in domain-model.md.
- **Impact**: None — gap closed.

## Missing States

### 1. Image-required validation on submit
- **Screen**: "At least one image recommended (enforced server-side for submission)"
- **API**: `CreateListingRequest` has no `images` field (images are uploaded separately via `POST /listings/{id}/images`)
- **Impact**: The create endpoint cannot validate BR-007 (≥1 image) at submission time because images don't exist yet — they are uploaded after the listing is created (listing ID needed for image association)
- **Workflow gap**: The current API requires a 2-step flow: `POST /listings` → `POST /listings/{id}/images`. If the user submits (action=submit) without uploading images, the listing goes to PENDING_APPROVAL with 0 images, violating BR-007
- **Fix**: Either (a) validate image count on submit action and return 400, or (b) support inline image upload in the create request as base64/multipart

### 2. No "Save as Draft" button
- **Screen**: Only "Hủy" and "Đăng tải" buttons shown
- **API**: `CreateListingRequest` has `action` field with values `save` (→ DRAFT) and `submit` (→ PENDING_APPROVAL)
- **Impact**: The API supports a distinction the UI doesn't expose. If the "Đăng tải" button maps to `submit`, then some required-image validation (BR-007) blocks submission, and the user has no way to save progress without uploading images first
- **Fix**: Either add a "Save as Draft" button to the screen, or make `action` default to `submit` and remove the `save` option from the API

## Naming Consistency

| Screen Label | API Field | Status |
|-------------|-----------|--------|
| Hình thức (BÁN/CHO THUÊ/SANG NHƯỢNG) | `transactionType` | ✓ No issue |
| Hoa hồng | `commissionType` + `commissionValue` | ✓ |
| Thành phố/Tỉnh | `city` | ✓ |
| Quận/Huyện | `district` | ✓ |
| Phường/Xã | `ward` | ✓ |
| Tên đường | `streetName` | ✓ |
| Số nhà | `houseNumber` | ✓ |
| Giá nhà | `price` | ✓ |
| Số điện thoại chủ nhà | `ownerPhone` | ✓ |
| Dài / Rộng | `areaLength` / `areaWidth` | ✓ |
| Số tầng / phòng ngủ / phòng tắm | `numFloors` / `numRooms` / `numBathrooms` | ✓ |
| Hướng nhà | `direction` | ✓ |
| Mặt tiền/Hẻm | `frontageType` | ✓ |
| Nhãn | `label` | ✓ |
| Đường vào | `roadWidth` | ✓ |
| Pháp lý | `legalStatus` | ✓ |
| Nội thất | `furnishing` | ✓ |
| Mô tả chi tiết | `description` | ✓ |
| Ảnh sản phẩm | `POST /listings/{id}/images` | ✓ |
| Video | `videoUrl` | ✓ |
| **Loại** (Property Type) | `propertyType` | ✓ (resolved) |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Location cascade | city/district/ward hierarchy (BR-013) | ✓ |
| Commission required | Both `commissionType` and `commissionValue` required | ✓ |
| Max 20 images | Enforced via BR-014 / IMG-C01 | ✓ |
| YouTube video | `videoUrl` with format validation | ✓ |
