# Story: Create Listing

## User Story

As an Agent
I want to create a new property listing with all required attributes
So that I can share the deal with other agents in the pool

## Description

A form allows the agent to input all property details: transaction type
(Sang nhượng / Cho thuê / Bán), address, price, area, room count, floors,
images, description, and commission. On save, the listing enters DRAFT status.

## Preconditions

- User is logged in as Agent

## Acceptance Criteria

### Happy Path

Given I am an Agent
When I click "Nhập hàng mới"
Then I see the listing creation form
When I fill in all required fields and upload at least one image
When I click "Save"
Then the listing is created in DRAFT status
And I am redirected to the listing detail page
And a product code is auto-generated

### Validation Rules

Given I attempt to submit without a required field (e.g., price)
When I click "Save"
Then I see a validation error on the empty field

Given I attempt to submit without any image
When I click "Submit for Approval"
Then I see an error: "At least one image is required"

Given I enter a non-numeric value in a numeric field
When I type into the price field
Then I see an input validation error

### Error Cases

Given the server fails to save the listing
When I click "Save"
Then I see an error message
And the entered data is preserved in the form

## Business Rules

- BR-001
- BR-007
- BR-008

## Related Entities

- Listing
- ListingImage

## Priority

Must Have
