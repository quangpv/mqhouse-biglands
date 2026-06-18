# BDD: Approve Cancellation

> **Story**: US-005-approve-cancellation
> **Priority**: Should Have
> **Related**: Listing, Approval, Notification, BR-005, AP-009, AP-010

## Acceptance Criteria
- Approver/Admin can confirm or reject a cancellation report
- Confirmation returns listing to CON_HANG (re-listed)
- Rejection leaves listing in DA_COC
- Agent receives notification

## Happy Paths

### H1: Approve cancellation (listing returns to pool)
```
Given I am logged in as Approver
And I am on the cancellation approval queue (Duyệt huỷ cọc)
And there is a cancellation report pending
When I review the cancellation reason
And I click "Confirm"
Then the listing status changes to CON_HANG (re-listed)
And the property is available again in the shared cart
And the agent receives a confirmation notification
```

### H2: Admin approves cancellation
```
Given I am logged in as Admin
When I approve a pending cancellation
Then the cancellation is confirmed
And the listing returns to CON_HANG
```

### H3: Reject cancellation
```
Given I am reviewing a cancellation report
When I click "Reject"
And I enter a rejection reason
And I confirm
Then the listing remains in DA_COC status
And the agent receives a rejection notification
```

## Error Cases

### E1: Reject without reason
```
Given I am rejecting a cancellation
When I click "Reject"
And I leave the reason empty
And I try to confirm
Then I see "Rejection reason is required"
```

## Edge Cases

### EC1: Concurrent approval
```
Given two approvers both open the same pending cancellation
When Approver A confirms the cancellation
And Approver B attempts to confirm the same cancellation
Then Approver B sees "This cancellation has already been processed"
```

### EC2: Approve cancellation on a listing that changed status
```
Given the listing status is no longer DA_COC (e.g., expired)
When I attempt to approve the cancellation
Then I see an error: "Listing status has changed since the cancellation was reported"
```

## Security Cases

### S1: Agent attempts to approve cancellation
```
Given I am logged in as Agent
When I navigate to the cancellation approval queue
Then I see "Bạn không có quyền truy cập trang này"
```

### S2: Agent attempts via API
```
Given I have an Agent session
When I send a POST request to the cancellation approval API
Then the response is HTTP 403
```
