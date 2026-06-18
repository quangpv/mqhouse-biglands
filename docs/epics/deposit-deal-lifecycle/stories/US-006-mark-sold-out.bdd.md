# BDD: Mark Listing as Sold-Out

> **Story**: US-006-mark-sold-out
> **Priority**: Must Have
> **Related**: Listing, DealEvent, BR-004, DD-006

## Acceptance Criteria
- Any authenticated user can report sold-out on any ACTIVE listing
- Confirmation step required before submission
- Listing must be in CON_HANG status
- Creates SOLD_OUT_REPORTED event and notifies approvers

## Happy Paths

### H1: Report sold-out successfully
```
Given I am logged in as an Agent
And I am viewing a listing with status CON_HANG
When I click "Báo hết hàng"
Then I am asked to confirm
When I confirm
Then a DealEvent of type SOLD_OUT_REPORTED is created
And approvers are notified
```

### H2: Any agent reports sold-out on any listing
```
Given I am logged in as Agent A
And I am viewing Agent B's ACTIVE listing
When I report sold-out
And I confirm
Then the sold-out report is created
```

### H3: Admin reports sold-out
```
Given I am logged in as Admin
When I report sold-out on any ACTIVE listing
Then the sold-out report is created
```

## Error Cases

### E1: Listing is already DA_COC (deposit confirmed)
```
Given the listing status is DA_COC
When I look for the "Báo hết hàng" button
Then the button is disabled or hidden
```

### E2: Listing is HET_HANG (already sold-out)
```
Given the listing status is HET_HANG
When I look for the "Báo hết hàng" button
Then the button is disabled or hidden
```

## Edge Cases

### EC1: Cancel the sold-out confirmation
```
Given I click "Báo hết hàng"
When the confirmation dialog appears
And I click "Cancel"
Then no event is created
And the listing remains ACTIVE
```

### EC2: Report sold-out on a listing with pending deposit
```
Given a deposit has been reported but not yet approved on this listing
When I look for the "Báo hết hàng" button
Then the button is disabled or hidden
```

### EC3: Sold-out report while another is pending
```
Given a sold-out report is already pending approval on this listing
When I attempt to report sold-out again
Then I see a message: "A sold-out report is already pending"
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I attempt to report sold-out
Then I am redirected to the login page
```
