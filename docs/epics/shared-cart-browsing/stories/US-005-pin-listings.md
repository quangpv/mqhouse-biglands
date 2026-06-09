# Story: Pin/Unpin Listings

## User Story

As an Agent
I want to pin listings to my personal watchlist
So that I can quickly find properties I'm interested in later

## Description

A heart/pin button on each listing card toggles pin status. Pinned listings
appear in the "Đã ghim" filter tab.

## Preconditions

- User is logged in

## Acceptance Criteria

### Happy Path

Given I am viewing a listing card
When I click the pin button
Then the listing is added to my pinned list
And the pin icon changes to the pinned state
When I click the pinned button again
Then the listing is removed from my pinned list

## Related Entities

- Listing

## Priority

Should Have
