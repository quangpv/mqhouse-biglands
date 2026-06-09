# Story: Manage Listing Status

## User Story

As an Agent
I want to delete a draft listing or withdraw an active one
So that I can remove listings that are no longer relevant

## Description

Agents can delete DRAFT listings entirely. For ACTIVE listings, the agent can
withdraw (return to DRAFT) or mark as sold-out pending approval.

## Preconditions

- User is logged in as Agent
- Listing belongs to current user

## Acceptance Criteria

### Happy Path

Given I have a DRAFT listing
When I click "Delete"
Then the listing is permanently removed

Given I have an ACTIVE listing
When I click "Withdraw"
Then the listing returns to DRAFT status

### Permission Rules

Given I am an Approver viewing any agent's listing
When I attempt to delete
Then the delete action is not available

## Related Entities

- Listing

## Priority

Should Have
