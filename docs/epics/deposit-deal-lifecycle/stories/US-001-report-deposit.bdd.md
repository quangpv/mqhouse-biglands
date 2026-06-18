# BDD: Report Customer Deposit

> **Story**: US-001-report-deposit
> **Priority**: Must Have
> **Related**: Listing, DealEvent, BR-001, BR-004, DD-001, DD-002
> **Contradiction Note**: C-02 (status change timing), C-09 (immediate vs pending) — resolved: immediate DA_COC on approver confirm. C-03 resolved: any agent.

## Acceptance Criteria
- Any authenticated user can report a deposit on any ACTIVE listing
- Customer name (≥2 chars), phone, and deposit amount (>0) are required
- Only one active deposit allowed per listing
- System creates DEPOSIT_REPORTED event and notifies approvers

## Happy Paths

### H1: Report deposit successfully
```
Given I am logged in as an Agent
And I am viewing a listing with status CON_HANG
When I click "Báo khách cọc"
Then I see a form with fields: customer name, customer phone, deposit amount
When I enter customer name "Nguyễn Văn A"
And I enter customer phone "0909123456"
And I enter deposit amount "50000000"
And I submit
Then a DealEvent of type DEPOSIT_REPORTED is created
And approvers are notified
```

### H2: Any agent can report on any listing
```
Given I am logged in as Agent A
And I am viewing a listing created by Agent B
When I report a deposit with valid data
Then the deposit is recorded successfully
```

### H3: Admin reports a deposit
```
Given I am logged in as Admin
And I am viewing an ACTIVE listing
When I report a deposit
Then the deposit is recorded
And approvers are notified
```

## Error Cases

### E1: Customer name too short
```
Given I am reporting a deposit
When I enter customer name "A"
And I submit
Then I see "Customer name must be at least 2 characters"
```

### E2: Deposit amount is zero
```
Given I am reporting a deposit
When I enter deposit amount "0"
And I submit
Then I see "Deposit amount must be greater than 0"
```

### E3: Deposit amount is negative
```
Given I am reporting a deposit
When I enter deposit amount "-1000000"
And I submit
Then I see "Deposit amount must be greater than 0"
```

### E4: Missing customer name
```
Given I am reporting a deposit
When I leave customer name empty
And I submit
Then I see "Customer name is required"
```

### E5: Missing deposit amount
```
Given I am reporting a deposit
When I leave deposit amount empty
And I submit
Then I see "Deposit amount is required"
```

## Edge Cases

### EC1: Duplicate pending deposit
```
Given another agent has already reported a deposit on this listing (pending approval)
When I attempt to report another deposit
Then I see "A deposit is already pending on this listing"
And no new DealEvent is created
```

### EC2: Listing is DA_COC (deposit already confirmed)
```
Given the listing status is DA_COC
When I look for the "Báo khách cọc" button
Then the button is disabled or hidden
```

### EC3: Listing is HET_HANG
```
Given the listing status is HET_HANG
When I look for the "Báo khách cọc" button
Then the button is disabled or hidden
```

### EC4: Deposit amount very large
```
Given I report a deposit with amount "9999999999999"
When I submit
Then the deposit is recorded with the exact amount
```

### EC5: Customer name with Vietnamese characters
```
Given I enter customer name "Nguyễn Thị Minh Khai 123"
When I submit
Then the deposit is recorded successfully
```

### EC6: Concurrent deposit reports
```
Given two agents both open the same ACTIVE listing
When Agent A submits a deposit report
And Agent B submits a deposit report concurrently
Then exactly one deposit report is created
And the other agent sees "A deposit is already pending on this listing"
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I attempt to report a deposit
Then I am redirected to the login page
```

### S2: Direct API call without permission
```
Given I have a valid Agent session
When I send a POST request to report a deposit on a non-existent listing
Then I receive HTTP 404
```

### S3: Deactivated user
```
Given my account is deactivated
When I attempt to log in
Then I cannot log in
```
