# BDD: Promote Listing to Hot

> **Story**: US-001-promote-to-hot
> **Priority**: Should Have
> **Related**: Listing entity, BR-009, HP-001, HP-002, HP-004

## Acceptance Criteria
- Admin can toggle "Hot" status on a listing
- Hot listings display "🔥 HOT" badge
- Hot listings appear at top of grid
- Only Admin can promote; only ACTIVE listings qualify

## Happy Paths

### H1: Promote listing to Hot
```
Given I am logged in as Admin
And I am viewing an ACTIVE listing
When I toggle "Hot" to on
Then the listing shows "🔥 HOT" badge on its card
And the listing appears at the top of the listing grid
```

### H2: Remove Hot status
```
Given the listing is currently marked as Hot
When I toggle "Hot" to off
Then the "🔥 HOT" badge is removed
And the listing appears in normal order
```

### H3: Promote from Hot Products management page
```
Given I am on the Hot Products management page
When I search for an ACTIVE listing
And I select it to promote
Then the listing is added to the hot list
And the badge appears on the homepage
```

## Error Cases

### E1: Promote a non-ACTIVE listing
```
Given I am viewing a listing with status DRAFT
When I attempt to toggle "Hot" to on
Then the toggle is disabled or I see an error
And the listing cannot be promoted to Hot
```

### E2: Promote when hot list is full
```
Given the hot list already has 14 items
When I attempt to promote another listing
Then I see a warning: "Hot list is full (max 14)"
```

## Edge Cases

### EC1: Demote listing and another auto-promotes
```
Given the hot list has 14 items
When I remove one listing from hot
Then I can immediately promote another listing
```

### EC2: Listing changes status while Hot
```
Given a listing is marked as Hot
When the listing status changes to HET_HANG (sold-out)
Then the listing is automatically removed from the hot list
And the "🔥 HOT" badge is removed
```

## Security Cases

### S1: Agent attempts to promote
```
Given I am logged in as Agent
When I attempt to toggle Hot status on a listing
Then the Hot toggle is not visible
```

### S2: Approver attempts to promote via API
```
Given I am logged in as Approver
When I send an API request to set isHot=true
Then the request is rejected with HTTP 403
```

### S3: Unauthenticated access to hot management
```
Given I am not logged in
When I navigate to /admin/san-pham-hot
Then I am redirected to the login page
```
