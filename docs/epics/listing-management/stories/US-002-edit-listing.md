# Story: Edit Listing

## User Story

As an Agent
I want to edit my existing listing
So that I can update property details or fix mistakes

## Description

Agents can edit their own listings in DRAFT or ACTIVE status. Edits to ACTIVE
listings may require re-approval depending on the field changed.

## Preconditions

- User is logged in as Agent
- Listing belongs to the current user
- Listing status is DRAFT or ACTIVE

## Acceptance Criteria

### Happy Path

Given I am viewing my own listing in DRAFT status
When I click "Edit"
Then the form is pre-filled with existing data
When I modify fields and click "Save"
Then the listing is updated

Given I am viewing my own listing in ACTIVE status
When I modify key fields (price, area, images)
Then the listing returns to PENDING_APPROVAL

### Permission Rules

Given I am viewing another agent's listing
When I attempt to edit
Then the edit button is not visible

## Related Entities

- Listing

## Priority

Must Have
