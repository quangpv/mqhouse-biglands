# Story: Notification Preferences

## User Story

As a platform user
I want to control which types of notifications I receive
So that I am not overwhelmed by noise

## Description

Users can enable or disable notification types: listing approved, listing
rejected, deposit reported, deposit confirmed, deal closed, sold-out approved.

## Preconditions

- User is logged in

## Acceptance Criteria

### Happy Path

Given I am on my profile/settings page
When I toggle off "Deposit reported" notifications
Then I no longer receive notifications when deposits are reported
When I toggle it back on
Then I resume receiving those notifications

## Related Entities

- Notification
- User (notification preferences)

## Priority

Could Have
