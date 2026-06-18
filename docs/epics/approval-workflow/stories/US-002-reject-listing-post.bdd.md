# BDD: Reject Listing Post

> **Story**: US-002-reject-listing-post
> **Priority**: Must Have
> **Related**: Listing, Approval, Notification, BR-005, BR-006

## Acceptance Criteria
- Approver can reject a listing with a reason
- Rejected listing returns to DRAFT
- Agent receives notification with rejection reason
- Rejection reason is required

## Happy Paths

### H1: Reject a listing with reason
```
Given I am logged in as Approver
And I am viewing a listing in PENDING_APPROVAL
When I click "Reject"
Then I am prompted to enter a rejection reason
When I enter "Incorrect price format" and confirm
Then the listing returns to DRAFT status
And the rejection reason is saved
And the agent receives a notification with the rejection reason
```

### H2: Reject a deposit report
```
Given I am viewing a pending deposit report
When I reject with reason "Proof of payment not clear"
Then the deposit report is rejected
And the listing remains in CON_HANG status
And the agent receives a notification with the rejection reason
```

### H3: Reject a cancellation request
```
Given I am viewing a pending cancellation request
When I reject with reason "Cancellation reason insufficient"
Then the cancellation request is rejected
And the deposit remains in place
And the agent receives a notification with the rejection reason
```

## Error Cases

### E1: Reject without reason
```
Given I click "Reject"
When I try to confirm without entering a reason
Then I see "Rejection reason is required"
```

### E2: Reject a listing that was already approved
```
Given another approver has already approved the listing
When I click "Reject"
Then I see "Listing already processed"
```

## Edge Cases

### EC1: Agent sees rejection reason on DRAFT
```
Given my listing was rejected with reason "Missing images"
When I view the DRAFT listing
Then I see the rejection reason displayed
And the form fields remain as submitted
```

## Security Cases

### S1: Agent cannot reject
```
Given I am logged in as Agent
When I attempt to reject a listing
Then the reject action is not available
```

### S2: Admin bypasses approval
```
Given I am logged in as Admin
When I create or edit a listing
Then the listing is published directly without requiring approval
And no rejection flow is applicable
```
