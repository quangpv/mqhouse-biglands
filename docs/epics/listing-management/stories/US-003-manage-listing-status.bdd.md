# BDD: Manage Listing Status

> **Story**: US-003-manage-listing-status
> **Priority**: Should Have
> **Related**: Listing, ES-003, ES-004

## Acceptance Criteria
- Owner can delete DRAFT listings (permanent)
- Owner can withdraw ACTIVE listings (return to DRAFT)
- Approver cannot delete listings

## Happy Paths

### H1: Delete a DRAFT listing
```
Given I am the owner of a listing in DRAFT status
When I click "Delete"
Then the listing is permanently removed
And I no longer see it in My Cart
```

### H2: Withdraw an ACTIVE listing
```
Given I am the owner of a listing in CON_HANG status
When I click "Withdraw"
Then the listing returns to DRAFT status
And the listing is no longer visible in the shared cart
```

## Error Cases

### E1: Delete an ACTIVE listing
```
Given I am the owner of a listing in CON_HANG status
When I look for the "Delete" button
Then the Delete button is not visible
```

### E2: Withdraw a DRAFT listing
```
Given the listing is already in DRAFT status
When I look for the "Withdraw" button
Then the Withdraw button is not visible
```

### E3: Delete a terminal-status listing
```
Given the listing status is HET_HANG
When I look for the "Delete" button
Then the Delete button is not visible
```

## Edge Cases

### EC1: Delete listing that has pending events
```
Given a DRAFT listing with no deal events
When I delete it
Then all associated images are also removed
```

### EC2: Withdraw listing with pending deposit
```
Given a CON_HANG listing has a pending deposit report
When I attempt to withdraw it
Then the withdrawal is allowed, and the listing returns to DRAFT
And the pending deposit report is invalidated
```

## Security Cases

### S1: Approver cannot delete
```
Given I am logged in as Approver
When I view any agent's listing
Then the delete action is not available
```

### S2: Another agent cannot delete
```
Given I am logged in as Agent A
And I am viewing Agent B's DRAFT listing
When I look for the "Delete" button
Then the Delete button is not visible
```
