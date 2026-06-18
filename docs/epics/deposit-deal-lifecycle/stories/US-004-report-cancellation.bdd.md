# BDD: Report Deposit Cancellation

> **Story**: US-004-report-cancellation
> **Priority**: Should Have
> **Related**: Listing, DealEvent, BR-002, BR-004, DD-004, DD-005
> **Contradiction Note**: C-03 resolved: any agent can report on any listing (BR-004).

## Acceptance Criteria
- Any authenticated user can report cancellation on a listing with confirmed deposit
- Cancellation reason is required
- Listing must be in DA_COC status
- Creates CANCELLATION_REPORTED event and notifies approvers

## Happy Paths

### H1: Report cancellation successfully
```
Given I am logged in as an Agent
And I am viewing a listing with status DA_COC (deposit confirmed)
When I click "Báo khách huỷ cọc"
Then I am prompted to enter a cancellation reason
When I enter reason "Khách hàng đổi ý, không mua nữa"
And I submit
Then a DealEvent of type CANCELLATION_REPORTED is created
And approvers are notified
```

## Error Cases

### E1: Submit cancellation without reason
```
Given I am reporting a cancellation
When I click submit without entering a reason
Then I see "Cancellation reason is required"
```

### E2: Listing is ACTIVE (no deposit)
```
Given the listing status is CON_HANG
When I look for the "Báo khách huỷ cọc" button
Then the button is disabled or hidden
```

### E3: Listing is HET_HANG
```
Given the listing status is HET_HANG
When I look for the "Báo khách huỷ cọc" button
Then the button is disabled or hidden
```

## Edge Cases

### EC1: Cancellation on already-cancelled listing
```
Given the listing status is HUY_COC (already cancelled)
When I look for the "Báo khách huỷ cọc" button
Then the button is disabled or hidden
```

### EC2: Long cancellation reason
```
Given I enter a very detailed cancellation reason spanning multiple paragraphs
When I submit
Then the cancellation report is created with the full reason
```

### EC3: Cancellation reason with special characters
```
Given I enter reason with Vietnamese characters "Khách huỷ do tìm được căn khác rẻ hơn"
When I submit
Then the cancellation report is created successfully
```

### EC4: Any agent reports cancellation on another agent's listing
```
Given I am Agent A viewing Agent B's DA_COC listing
When I report cancellation with a valid reason
Then the cancellation report is created
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I attempt to report a cancellation
Then I am redirected to the login page
```
