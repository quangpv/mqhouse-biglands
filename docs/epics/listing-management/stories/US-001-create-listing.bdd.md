# BDD: Create Listing

> **Story**: US-001-create-listing
> **Priority**: Must Have
> **Related**: Listing, ListingImage, BR-001, BR-007, BR-008, BR-012, BR-013, BR-014
> **Contradiction Note**: C-01 (commission required for all vs SANG_NHUONG/BAN), C-05 (save vs submit), C-06 (address fields), C-07 (commission required vs optional), C-08 (image required vs recommended), C-11 (admin creates listings)

## Acceptance Criteria
- Agent can create a new listing via the creation form
- Form includes all property attributes, images, and video
- Product code is auto-generated
- Listing is saved as DRAFT on Save or PENDING_APPROVAL on Submit
- All required fields must be validated

## Happy Paths

### H1: Create listing and save as Draft
```
Given I am logged in as an Agent
When I click "Nhập hàng mới"
Then I see the listing creation form
When I select transaction type "BÁN"
And I fill in price "5000000000"
And I fill in commission "2" with type "%"
And I select city "Hồ Chí Minh"
And I select district "Quận 1"
And I select ward "Phường Bến Nghé"
And I enter street name "Nguyễn Huệ"
And I enter house number "123"
And I enter area width "5"
And I enter area length "20"
And I enter total floors "4"
And I enter bedrooms "8"
And I enter bathrooms "6"
And I enter description "CHDV building in District 1"
And I upload at least one image
And I enter owner phone "0909123456"
And I click "Save"
Then the listing is created in DRAFT status
And a product code is auto-generated
And I am redirected to the product detail page
```

### H2: Submit listing for approval directly
```
Given I am on the create listing form
When I fill in all required fields
And I upload at least one image
And I click "Submit for Approval"
Then the listing is created in PENDING_APPROVAL status
And approvers are notified
```

### H3: Create listing with optional fields
```
Given I am creating a listing
When I fill in all required fields
And I enter direction "Đông"
And I select frontage type "Mặt Tiền"
And I select label "Thang máy"
And I enter road width "8"
And I enter legal status "Sổ hồng"
And I enter furnishing "Đầy đủ nội thất cao cấp"
And I upload 5 images
And I add a YouTube video link
And I submit
Then the listing is created with all optional attributes saved
```

## Error Cases

### E1: Missing required field (price)
```
Given I am creating a listing
When I leave the price field empty
And I click "Submit for Approval"
Then I see "Price is required"
```

### E2: No images uploaded
```
Given I am creating a listing
When I fill in all other required fields
And I upload no images
And I click "Submit for Approval"
Then I see "At least one image is required"
```

### E3: Non-numeric price
```
Given I am creating a listing
When I enter price "abc"
Then I see an input validation error on the price field
```

### E4: Missing commission
```
Given I am creating a listing
When I leave commission fields empty
And I click "Submit for Approval"
Then I see "Commission is required"
```

### E5: Floor cascade not completed
```
Given I select city "Hồ Chí Minh"
When I do not select a district
And I attempt to select a ward
Then the ward field is disabled
```

## Edge Cases

### EC1: Maximum images (20)
```
Given I am creating a listing
When I upload 20 images
And I attempt to upload one more
Then I see "Maximum 20 images allowed"
```

### EC2: Max field lengths
```
Given I enter the maximum allowed text in the description field
When I submit
Then the listing is created with the full description
```

### EC3: Delete a draft listing
```
Given I have a DRAFT listing
When I navigate to My Cart
And I click "Delete" on the DRAFT listing
Then the listing is permanently removed
```

### EC4: Video with different URL format
```
Given I am creating a listing
When I enter a YouTube short URL "https://youtu.be/RzVvThhjAKw"
And I submit
Then the listing is created with the video link saved
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I navigate to /gio-hang/tao
Then I am redirected to the login page
```

### S2: Create listing with invalid session
```
Given my session has expired
When I attempt to submit the create listing form
Then I am redirected to the login page
And the form data is preserved
```
