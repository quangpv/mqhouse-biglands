# BDD: Receive Notifications

> **Story**: US-001-receive-notification
> **Priority**: Must Have
> **Related**: Notification, BR-010

## Acceptance Criteria
- Notifications are generated automatically on key events
- A badge shows unread notification count
- Notification contains event type, listing title, and timestamp

## Happy Paths

### H1: Agent receives notification on listing approved
```
Given I am logged in as Agent
When my listing is approved by an approver
Then I receive a notification: "Your listing [title] has been approved"
And the notification has type "LISTING_APPROVED"
And the notification badge shows an incremented count
```

### H2: Agent receives notification on listing rejected
```
Given I am logged in as Agent
When my listing is rejected by an approver
Then I receive a notification: "Your listing [title] has been rejected: [reason]"
And the notification badge shows an incremented count
```

### H3: Agent receives notification on deposit reported
```
Given I am logged in as Approver
When an agent reports a deposit on a listing
Then I receive a notification: "New deposit report on [listing title]"
```

### H4: Agent receives notification on deposit confirmed
```
Given I am logged in as Agent
When my deposit report is approved
Then I receive a notification: "Deposit on [listing title] has been confirmed"
```

### H5: Agent receives notification on deal closed
```
Given I am logged in as Agent
When my deal closure is approved
Then I receive a notification: "Deal on [listing title] has been closed"
```

### H6: Agent receives notification on cancellation confirmed
```
Given I am logged in as Agent
When my cancellation request is approved
Then I receive a notification: "Cancellation on [listing title] has been confirmed"
```

### H7: Agent receives notification on sold-out confirmed
```
Given I am logged in as Agent
When my sold-out report is approved
Then I receive a notification: "[listing title] has been marked as sold out"
```

## Error Cases

### E1: Notification delivery failure
```
Given a notification is generated
And the notification service fails
Then the event is still processed
And a retry is scheduled
```

## Edge Cases

### EC1: Multiple notifications for same event
```
Given I generate a deposit report
And the approver confirms it
Then I receive exactly one notification for the confirmation
And no duplicate notifications
```

### EC2: Notifications persist after listing deletion
```
Given a listing is deleted
And I had a notification about that listing
When I view my notifications
Then the notification still appears
And I can see the listing title in the notification text
```

## Security Cases

### S1: User cannot see another user's notifications
```
Given I am logged in as Agent A
When I inspect my notification list
Then I only see notifications addressed to me
And I cannot see Agent B's notifications
```

### S2: Unauthenticated access
```
Given I am not logged in
When I navigate to the notifications page
Then I am redirected to the login page
```
