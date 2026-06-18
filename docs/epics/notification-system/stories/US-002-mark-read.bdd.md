# BDD: Mark Notifications as Read

> **Story**: US-002-mark-read
> **Priority**: Should Have
> **Related**: Notification

## Acceptance Criteria
- Clicking a notification marks it as read and navigates to the related item
- "Mark All as Read" marks all notifications as read
- Read and unread notifications are visually distinct
- Badge count updates correctly

## Happy Paths

### H1: Mark single notification as read by clicking
```
Given I have unread notifications
When I click on a notification
Then the notification is marked as read
And the notification badge count decreases by 1
And I am navigated to the related listing or event
```

### H2: Mark all notifications as read
```
Given I have multiple unread notifications
When I click "Mark All as Read"
Then all my notifications are marked as read
And the notification badge count becomes 0
```

### H3: Notification remains visible after reading
```
Given I have marked a notification as read
When I open my notification list
Then the notification is still visible
And it appears with a different visual style (faded or dimmed)
```

## Error Cases

### E1: Mark all as read when none unread
```
Given I have 0 unread notifications
When I click "Mark All as Read"
Then nothing changes
```

## Edge Cases

### EC1: Click notification with deleted listing
```
Given I receive a notification about a listing
And the listing is later deleted
When I click the notification
Then I am navigated to a page showing "Listing not found"
And the notification is still marked as read
```

### EC2: Rapid double-click on a notification
```
Given I have an unread notification
When I click it twice rapidly
Then the notification is marked as read exactly once
And the badge count decreases by exactly 1
```

## Security Cases

### S1: Mark read only own notifications
```
Given I am logged in as Agent A
When I click "Mark All as Read"
Then only my notifications are affected
And Agent B's notifications remain unchanged
```
