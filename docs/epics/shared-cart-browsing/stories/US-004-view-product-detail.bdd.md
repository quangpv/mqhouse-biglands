# BDD: View Product Detail

> **Story**: US-004-view-product-detail
> **Priority**: Must Have
> **Related**: Listing, ListingImage, LV-004

## Acceptance Criteria
- All authenticated users can view any listing's full detail
- Image gallery with navigation
- Deal action buttons shown with context-dependent states
- Agent contact info visible
- Reviews section displayed

## Happy Paths

### H1: View product detail as Agent
```
Given I am logged in as an Agent
When I click on a listing card on the shared cart
Then I navigate to /san-pham/:id
And I see the image gallery with navigation arrows
And I see the title with HOT badge (if promoted)
And I see transaction type badge and status badge
And I see the price, commission, area, rooms, bathrooms, floors
And I see the full address
And I see the agent name and listing date
And I see deal action buttons
```

### H2: View product detail as listing owner
```
Given I am logged in as the owner of this listing
When I view the product detail
Then I see the "Chỉnh sửa lại thông tin hàng" (Edit) button
And I see all 4 deal action buttons
```

### H3: View product detail as non-owner
```
Given I am viewing another agent's listing
When I view the product detail
Then I see deal action buttons
But I do NOT see the Edit button
```

### H4: View listing with DA_COC status
```
Given the listing status is DA_COC
When I view the product detail
Then the "Báo khách cọc" button is disabled
And "Báo hết hàng" button is disabled
And "Báo khách chốt hàng" button is enabled
And "Báo khách huỷ cọc" button is enabled
```

## Error Cases

### E1: Non-existent listing
```
Given I navigate to /san-pham/non-existent-id
When I attempt to view the detail
Then I see a "Listing not found" error
```

## Security Cases

### S1: Unauthenticated access
```
Given I am not logged in
When I attempt to navigate to /san-pham/:id
Then I am redirected to the login page
```
