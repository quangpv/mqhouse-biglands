# Story: Filter Listings by Category

## User Story

As an Agent
I want to filter listings by tabs: All, Pinned, Hot
So that I can focus on the most relevant subset

## Description

Three tabs at the top of the listing grid: "Tất cả loại hàng" (All),
"Đã ghim" (Pinned), "Hàng Hot" (Hot). Each shows the count.

## Preconditions

- User is logged in

## Acceptance Criteria

### Happy Path

Given I am on the shared cart page
When I click the "Hàng Hot" tab
Then I see only hot listings
When I click the "Đã ghim" tab
Then I see only listings I have pinned
When I click "Tất cả loại hàng" tab
Then I see all active listings again

### Validation Rules

Given I have no pinned listings
When I switch to the "Đã ghim" tab
Then I see an empty state

## Related Entities

- Listing

## Priority

Should Have
