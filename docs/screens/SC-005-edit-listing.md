# Edit Listing

## Purpose

Edit an existing listing's attributes. Available to the listing owner (agent).

## Route

`/gio-hang/:id/chinh-sua`

## Trigger

Edit action on Product Detail page (owner only)

## Components

Same form layout as Create Listing (SC-004), pre-filled with current listing data.

### Additional Behaviors

- Status-dependent: some fields may be locked after approval
- Save creates a new version / updates in place
- If listing is in DRAFT or REJECTED status, submit for approval again

### Form Fields

Identical to Create Listing (SC-004):
- Transaction type (locked after submission?)
- Title, price, commission, area, rooms, bathrooms, floors
- Address, ward, district, city
- Direction, road width, legal status, elevator, furnishing
- Description
- Images (add/remove/reorder)

### Actions

- "Save" — persist changes
- "Submit for Approval" — if in DRAFT or REJECTED status

## Entities

- Listing
- ListingImage

## Related Stories

- Listing Management US-002 (edit listing)

## Navigation Links

- Product Detail `/san-pham/:id` (after save)
- Shared Cart Home `/`
