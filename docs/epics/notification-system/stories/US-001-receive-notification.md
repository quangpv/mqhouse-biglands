# Story: Receive Notifications

## User Story

As a platform user
I want to receive notifications when events happen on my listings or tasks
So that I can stay informed without manually checking

## Description

Notifications are created automatically when key events occur: listing
approved/rejected, deposit reported/confirmed, deal closed, cancellation
confirmed, sold-out confirmed. A badge on the notification icon shows the
unread count.

## Preconditions

- User is logged in

## Acceptance Criteria

### Happy Path

Given I am an Agent
When my listing is approved
Then I receive a notification: "Your listing [title] has been approved"
And the notification badge shows an incremented count

Given I am an Approver
When an agent reports a deposit
Then I receive a notification: "New deposit report on [listing title]"

## Business Rules

- BR-010

## Related Entities

- Notification

## Priority

Must Have
