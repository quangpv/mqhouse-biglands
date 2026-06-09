# Story: Browse Listings

## User Story

As an Agent
I want to browse all available listings in a paginated grid
So that I can quickly scan what properties are on the market

## Description

The shared cart homepage displays property listings as cards in a grid layout.
Each card shows the title, price, commission, address, area, room count,
bathroom count, floor count, agent name, date, and a thumbnail image.

## Preconditions

- User is logged in as Agent, Approver, or Admin

## Acceptance Criteria

### Happy Path

Given I am logged in as an Agent
When I navigate to the homepage
Then I see a grid of listing cards sorted by recency
And I see the total count of listings displayed
And I can click "Next" to view subsequent pages
And I can click page numbers to jump to a specific page

### Validation Rules

Given the shared cart has 0 listings
When I view the homepage
Then I see an empty state message

### Error Cases

Given the server is unavailable
When I navigate to the homepage
Then I see a loading state or error message

### Permission Rules

Given I am not logged in
When I navigate to the homepage
Then I am redirected to the login page

## Business Rules

- BR-001
- BR-003

## Related Entities

- Listing

## Priority

Must Have
