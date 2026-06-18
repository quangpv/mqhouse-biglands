# BDD: Bulk Approve Listings

> **Story**: US-003-bulk-approve
> **Priority**: Could Have
> **Related**: Listing, Approval, Notification, BR-005

## Acceptance Criteria
- Approver can select multiple pending listings and approve them at once
- Each listing agent receives individual notification
- Bulk reject is not supported (rejection requires individual reason)
- At least one listing must be selected

## Happy Paths

### H1: Bulk approve multiple listings
```
Given I am logged in as Approver
And I am on the approval queue page
And there are at least 2 listings pending approval
When I check the checkboxes for 2 listings
And I click "Approve Selected"
Then both listings change to CON_HANG status
And each listing's agent receives a notification
```

### H2: Bulk approve all by select-all
```
Given there are multiple pending listings
When I click the "Select All" checkbox
And I click "Approve Selected"
Then all visible pending listings are approved
```

## Error Cases

### E1: No listings selected
```
Given I am on the approval queue page
When I click "Approve Selected" without selecting any
Then I see "Please select at least one listing"
```

### E2: Partial failure in bulk approve
```
Given I select 5 listings to approve
And one listing has conflicting data
When I click "Approve Selected"
Then the valid listings are approved
And I see a message: "4 approved, 1 failed"
And the failed listing remains in PENDING_APPROVAL
```

## Edge Cases

### EC1: Bulk approve across pages
```
Given there are pending listings on page 2
When I select listings only on page 1
And I approve
Then only page 1 listings are approved
```

### EC2: Mixed transaction types in bulk
```
Given the approval queue contains both BAN and CHO_THUE listings
When I select all and approve
Then all selected listings are approved regardless of type
```

## Security Cases

### S1: Agent cannot bulk approve
```
Given I am logged in as Agent
When I look for the bulk approve controls
Then they are not visible
```
