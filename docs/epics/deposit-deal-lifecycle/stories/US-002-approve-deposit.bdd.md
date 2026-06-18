# BDD: Approve Deposit Report

> **Story**: US-002-approve-deposit
> **Priority**: Must Have
> **Related**: Listing, DealEvent, Approval, Notification, BR-005, AP-005, AP-006
> **Contradiction Note**: C-09 (immediate DA_COC vs intermediate pending)

## Acceptance Criteria
- Approver/Admin can confirm or reject a deposit report
- Confirmation changes listing status to DA_COC
- Rejection returns listing to CON_HANG
- Agent receives notification

## Happy Paths

### H1: Approve a deposit
```
Given I am logged in as Approver
And I am on the deposit approval queue (Duyệt báo cọc)
And there is a listing with a pending deposit report
When I review the deposit details
And I click "Confirm"
Then the listing status changes to DA_COC
And the agent who reported receives a confirmation notification
And a DealEvent of type DEPOSIT_CONFIRMED is created
```

### H2: Admin approves a deposit
```
Given I am logged in as Admin
And I am on the deposit approval queue
When I approve a pending deposit
Then the deposit is confirmed
And the agent is notified
```

### H3: Reject a deposit
```
Given I am reviewing a deposit report
When I click "Reject"
And I enter a rejection reason
And I confirm
Then the listing returns to CON_HANG status
And the agent receives a rejection notification
And no DEPOSIT_CONFIRMED event is created
```

## Error Cases

### E1: Reject without reason
```
Given I am rejecting a deposit
When I click "Reject"
And I leave the reason empty
And I try to confirm
Then I see "Rejection reason is required"
```

## Edge Cases

### EC1: Concurrent approval
```
Given two approvers both open the same pending deposit
When Approver A confirms the deposit
And Approver B attempts to confirm the same deposit
Then Approver B sees "This deposit has already been processed"
And the listing is already in DA_COC status
```

### EC2: Approve a deposit on a listing that is no longer ACTIVE
```
Given the listing status changed from CON_HANG since the deposit was reported
When I attempt to approve the deposit
Then I see an error: "Listing is no longer available for deposit"
```

### EC3: Reject and re-report cycle
```
Given a deposit was rejected
When the agent reports a new deposit on the same listing
And I approve it
Then the deposit is confirmed successfully
And the listing status changes to DA_COC
```

## Security Cases

### S1: Agent attempts to approve deposit
```
Given I am logged in as Agent
When I navigate to the deposit approval queue
Then I see "Bạn không có quyền truy cập trang này"
```

### S2: Agent attempts to approve via API
```
Given I have an Agent session token
When I send a POST request to the deposit approval API
Then the response is HTTP 403
```
