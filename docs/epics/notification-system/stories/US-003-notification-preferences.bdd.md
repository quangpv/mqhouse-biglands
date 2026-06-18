# BDD: Notification Preferences

> **Story**: US-003-notification-preferences
> **Priority**: Could Have
> **Related**: Notification, User

## Acceptance Criteria
- User can toggle notification types on/off from profile/settings
- Toggling off a type suppresses notifications of that type going forward
- Toggling on resumes notifications
- Preferences are persisted

## Happy Paths

### H1: Disable a notification type
```
Given I am logged in
And I am on my profile/settings page
When I toggle off "Deposit reported" notifications
Then the setting is saved
And I no longer receive notifications when deposits are reported
```

### H2: Re-enable a notification type
```
Given I have disabled "Listing approved" notifications
When I toggle "Listing approved" back on
Then I resume receiving those notifications
```

### H3: Default preferences
```
Given I am a new user
When I view my notification preferences
Then all notification types are enabled by default
```

## Error Cases

### E1: Save failure
```
Given I toggle a notification preference
And the server fails to save
Then I see "Failed to save preference"
And the toggle reverts to its previous state
```

## Edge Cases

### EC1: Preferences affect future notifications only
```
Given I disable "Listing rejected" notifications
And I already have 3 unread "listing rejected" notifications
When a new listing is rejected
Then I do not receive a notification for the new rejection
But the 3 existing notifications remain unread
```

### EC2: Preferences persist across sessions
```
Given I disable "Sold-out confirmed" notifications
When I log out and log back in
Then my preferences are still applied
```

### EC3: Toggle all off
```
Given I toggle off all notification types
When a new event occurs
Then I receive no notifications
```

## Security Cases

### S1: User cannot modify another user's preferences
```
Given I am logged in as Agent A
When I attempt to modify Agent B's preferences
Then the operation is denied
```
