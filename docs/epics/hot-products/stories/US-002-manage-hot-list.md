# Story: Manage Hot Products List

## User Story

As an Admin
I want to view and manage all hot products in one place
So that I can curate the hot list effectively

## Description

An admin page lists all products currently marked as Hot. Admin can remove
items from the hot list or reorder them.

## Preconditions

- User is logged in as Admin
- At least one listing is marked as Hot

## Acceptance Criteria

### Happy Path

Given I am an Admin
When I navigate to the Hot Products management page
Then I see a list of all listings with "Hot" status
When I click "Remove" on a listing
Then the listing is no longer hot
And the hot list updates

## Related Entities

- Listing

## Priority

Should Have
