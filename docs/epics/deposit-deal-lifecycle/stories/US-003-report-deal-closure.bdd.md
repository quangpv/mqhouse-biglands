# BDD: Report Deal Closure

> **Story**: US-003-report-deal-closure
> **Priority**: Should Have
> **Related**: Listing, DealEvent, BR-003, BR-004, DD-003
> **Contradiction Note**: C-03 resolved: any agent can report on any listing (BR-004).

## Acceptance Criteria
- Any authenticated user can report closure on a listing with confirmed deposit
- Listing must be in DA_COC status
- Creates CLOSURE_REPORTED event and notifies approvers

## Happy Paths

### H1: Report deal closure successfully
```
Given I am logged in as an Agent
And I am viewing a listing with status DA_COC (deposit confirmed)
When I click "Báo khách chốt hàng"
Then I see a closure form with optional notes
When I enter notes "Khách đã thanh toán đủ"
And I submit
Then a DealEvent of type CLOSURE_REPORTED is created
And approvers are notified
```

### H2: Report closure without notes
```
Given the listing status is DA_COC
When I click "Báo khách chốt hàng"
And I submit without entering notes
Then the closure report is created successfully
```

## Error Cases

### E1: Listing is ACTIVE (no deposit)
```
Given the listing status is CON_HANG
When I look for the "Báo khách chốt hàng" button
Then the button is disabled or hidden
```

### E2: Listing is HET_HANG
```
Given the listing status is HET_HANG
When I look for the "Báo khách chốt hàng" button
Then the button is disabled or hidden
```

## Edge Cases

### EC1: Report closure after cancelled deposit
```
Given the listing status is HUY_COC (cancelled)
When I look for the "Báo khách chốt hàng" button
Then the button is disabled or hidden
```

### EC2: Closure report while another closure is pending
```
Given a closure has already been reported (pending approval)
When I attempt to report closure again
Then I see an error: "A closure report is already pending"
```

### EC3: Any agent reports closure on another agent's listing
```
Given I am Agent A
And I am viewing a DA_COC listing created by Agent B
When I report closure
Then the closure report is created successfully
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I attempt to access the closure report function
Then I am redirected to the login page
```
