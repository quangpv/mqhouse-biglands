# Story: Mark Notifications as Read

## User Story

As a platform user
I want to mark notifications as read
So that I can track what I have already seen

## Description

Users can click a notification to mark it as read, or use "Mark All as Read".
Read notifications are visually distinct from unread ones.

## Preconditions

- User is logged in
- User has at least one unread notification

## Acceptance Criteria

### Happy Path

Given I have unread notifications
When I click on a notification
Then the notification is marked as read
And the badge count decreases by 1

Given I have multiple unread notifications
When I click "Mark All as Read"
Then all my notifications are marked as read
And the badge count becomes 0

## Related Entities

- Notification

## Priority

Should Have
