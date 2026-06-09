# Create Listing

## Purpose

Form to create a new property listing with all required attributes.

## Route

`/gio-hang/tao`

## Trigger

"Nhập hàng mới" button on Shared Cart Home or My Cart page

## Form Fields

### Tiêu đề sản phẩm (Product Title)
- Textbox (NOT required)

### Hình thức (*) (Transaction Type)
- Combobox (default: BÁN)
- Options: BÁN / CHO THUÊ / SANG NHƯỢNG

### Loại (*) (Property Type)
- Combobox (empty until selection made)

### Hoa hồng (*) (Commission)
- Spinbutton for value
- Toggle buttons: "%" / "VNĐ"
- Supports both percentage and fixed amount

### Location Cascade
- **Thành phố/Tỉnh (*)** — Combobox (default: Hồ Chí Minh)
- **Quận/Huyện (*)** — Combobox (populated after city selection)
- **Phường/Xã (*)** — Combobox (disabled until district selected)

### Tên đường (*) (Street Name)
- Textbox

### Số nhà (*) (House Number)
- Textbox

### Giá nhà (*) (Price)
- Spinbutton "Nhập giá" (VND)

### Số điện thoại chủ nhà (*) (Owner Phone)
- Textbox

### Property Dimensions
- **Dài (*)** (Length) — spinbutton (m)
- **Rộng (*)** (Width) — spinbutton (m)
- **Số tầng (*)** (Floors) — spinbutton
- **Số phòng ngủ (*)** (Bedrooms) — spinbutton
- **Số phòng tắm, vệ sinh (*)** (Bathrooms) — spinbutton

### Optional Attributes
- **Hướng nhà** (Direction) — combobox: "Chọn Hướng nhà"
- **Mặt tiền/Hẻm** (Street front / Alley) — combobox: "Chọn"
- **Nhãn** (Label/Tag) — combobox: "Chọn nhãn" (e.g., Thang máy, Nhà mới, Vị trí đẹp)
- **Đường vào** (Road width) — spinbutton
- **Pháp lý** (Legal docs) — textbox
- **Nội thất** (Furniture) — textbox

### Mô tả chi tiết (*) (Description)
- Textbox (required)

### Media
- **Ảnh sản phẩm** — Add image button (max 20 images per listing)
- **Video** — Add video button + textbox for YouTube link
  - Placeholder: "Nhập link video"
  - Example: "https://www.youtube.com/watch?v=RzVvThhjAKw"

## Actions
- "Hủy" (Cancel) — discards form
- "Đăng tải" (Post/Submit) — submits for approval

## Validation

- All (*) fields are required
- Price, area dimensions, address required
- Commission required for all transaction types
- Numeric validation on price/area/room fields
- At least one image recommended (enforced server-side for submission)
- Location cascade: district depends on city, ward depends on district

## Entities

- Listing
- ListingImage

## Related Stories

- Listing Management US-001 (create listing)

## Navigation Links

- Shared Cart Home `/` (after save)
- My Cart `/gio-hang` (after save)
- Product Detail `/san-pham/:id` (after save)
