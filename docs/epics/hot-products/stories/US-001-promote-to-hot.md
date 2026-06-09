# Story: Promote Listing to Hot

## User Story

As an Admin
I want to mark a listing as Hot
So that it gets priority visibility with a badge

## Description

From the listing detail page or from the Hot Products admin page, admin can
toggle the "Hot" status. Hot listings display a "🔥 HOT" badge and appear
before non-hot listings in the shared cart.

## Preconditions

- User is logged in as Admin
- Listing is in ACTIVE status

## Acceptance Criteria

### Happy Path

Given I am an Admin viewing a listing
When I toggle "Hot" to on
Then the listing shows "🔥 HOT" badge on its card
And the listing appears at the top of the listing grid

Given I am an Admin
When I toggle "Hot" to off
Then the "🔥 HOT" badge is removed
And the listing appears in normal order

## Business Rules

- BR-003
- BR-009

## Related Entities

- Listing

## Priority

Should Have
