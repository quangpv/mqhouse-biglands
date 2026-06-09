# Story: Search Listings

## User Story

As an Agent
I want to search listings by product code, title, content, or address
So that I can quickly find a specific property

## Description

A search textbox allows full-text search across key listing fields. Results
update to show only matching listings.

## Preconditions

- User is logged in

## Acceptance Criteria

### Happy Path

Given I am on the shared cart page
When I type a search term into the search box
Then the listing grid updates to show only matching results
And the result count updates accordingly

### Validation Rules

Given my search term matches no listings
When I submit the search
Then I see an empty results message with the search term

### Error Cases

Given my search term contains special characters
When I submit the search
Then the search is executed safely without errors

## Business Rules

- Search covers: product code, title, description, address, ward, district

## Related Entities

- Listing

## Priority

Must Have
