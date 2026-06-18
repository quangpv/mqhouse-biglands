# BDD: Approve Listing Post

> **Story**: US-001-approve-listing-post
> **Priority**: Must Have
> **Related**: Listing, Approval, Notification, BR-005, BR-006

## Acceptance Criteria
- Approver can approve listings from a dedicated queue
- Listing changes from PENDING_APPROVAL to ACTIVE (CON_HANG)
- Listing agent receives notification
- Double-approval race condition is prevented

## Happy Paths

### H1: Approve a single listing
```
Given I am logged in as Approver
And there are listings in PENDING_APPROVAL status
When I navigate to the approval queue
Then I see a list of listings pending approval
When I click on a listing
Then I see the full listing details
When I click "Approve"
Then the listing status changes to CON_HANG
And the listing agent receives a notification
And a notification is created in the agent's notification list
```

### H2: Approve a deposit report
```
Given I am logged in as Approver
And there is a deposit report pending approval
When I navigate to the deposit approval queue
Then I see the deposit with full listing details
When I click "Approve"
Then the listing status changes to DA_COC
And the deposit report is marked as confirmed
And the agent receives a notification
```

### H3: Approve a cancellation request
```
Given I am logged in as Approver
And there is a cancellation request pending approval
When I navigate to the cancellation approval queue
Then I see the cancellation request with reason
When I click "Approve"
Then the listing returns to CON_HANG status
And the cancellation is marked as confirmed
And the agent receives a notification
```

### H4: Approve a sold-out report
```
Given I am logged in as Approver
And there is a sold-out report pending approval
When I navigate to the sold-out approval queue
Then I see the sold-out request
When I click "Approve"
Then the listing status changes to HET_HANG (terminal)
And the agent receives a notification
```

## Error Cases

### E1: Approve listing with missing required data
```
Given the listing is missing required business data
When I click "Approve"
Then I see "Cannot approve: missing required data"
And the listing remains in PENDING_APPROVAL
```

### E2: Double-approve by two approvers
```
Given approver A and approver B both view the same pending listing
When approver A clicks "Approve"
And then approver B clicks "Approve"
Then approver A's action succeeds
And approver B sees "Listing already processed"
```

### E3: Approve a listing that is no longer pending
```
Given the listing has already been processed by another approver
When I click "Approve"
Then I see an error message
```

## Edge Cases

### EC1: Approve across different transaction type queues
```
Given I am viewing the BAN queue
When I approve a listing
Then only BAN listings are affected
And other queue listings remain unchanged
```

### EC2: Network failure during approve
```
Given I click "Approve"
And the network request fails
Then the listing remains in PENDING_APPROVAL
And I see a retry prompt
```

## Security Cases

### S1: Agent cannot access approval queue
```
Given I am logged in as Agent
When I navigate to the approval queue page
Then I see a permission denied error or am redirected
```

### S2: Approver cannot approve their own listing
```
Given I am logged in as Approver
And I am also the listing owner
When I attempt to approve my own listing
Then I see "Cannot approve your own listing"
```

### S3: Unauthenticated access
```
Given I am not logged in
When I navigate to the approval queue
Then I am redirected to the login page
```
