# BDD: Edit Listing

> **Story**: US-002-edit-listing
> **Priority**: Must Have
> **Related**: Listing, BR-004, ES-001, ES-002
> **Contradiction Note**: AR-03 (which fields trigger re-approval), AR-04 (transaction type locked?) — C-03 resolved: any agent.

## Acceptance Criteria
- Listing owner can edit their own listings
- DRAFT edits save without re-approval
- ACTIVE edits to key fields (price, area, images) trigger re-approval
- Non-owners cannot see the Edit button

## Happy Paths

### H1: Edit DRAFT listing without re-approval
```
Given I am the owner of a listing in DRAFT status
When I click "Edit"
Then the form is pre-filled with existing data
When I modify the title and description
And I click "Save"
Then the listing is updated
And the listing remains in DRAFT status
```

### H2: Edit ACTIVE listing — non-key field
```
Given I am the owner of a listing in CON_HANG status
When I edit the description field
And I click "Save"
Then the listing is updated
And the listing remains in CON_HANG status
```

### H3: Edit ACTIVE listing — key field triggers re-approval
```
Given I am the owner of a listing in CON_HANG status
When I modify the price from "5000000000" to "6000000000"
And I click "Save"
Then the listing status changes to PENDING_APPROVAL
And the listing must be re-approved by an approver
```

### H4: Edit DRAFT and submit for approval
```
Given I am editing a DRAFT listing
When I make changes
And I click "Submit for Approval"
Then the listing status changes to PENDING_APPROVAL
```

## Error Cases

### E1: Non-owner attempts to edit
```
Given I am viewing another agent's listing
When I look for the "Edit" button
Then the Edit button is not visible
```

### E2: Edit a terminal-status listing
```
Given the listing status is HET_HANG (terminal)
When I look for the "Edit" button
Then the Edit button is not visible
```

### E3: Change transaction type
```
Given I am editing a listing
When I attempt to change the transaction type
Then the transaction type field is locked
```

## Edge Cases

### EC1: Edit with no changes
```
Given I am editing my own listing
When I click "Save" without making any changes
Then the listing data remains unchanged
And no status change occurs
```

### EC2: Edit images on ACTIVE listing
```
Given I am editing my CON_HANG listing
When I remove the primary image
And I upload a new image
And I click "Save"
Then the listing returns to PENDING_APPROVAL
```

### EC3: Rapid successive edits
```
Given I edit a DRAFT listing
And I save
And I immediately edit again
Then the second edit pre-fills the form with the first edit's changes
```

## Security Cases

### S1: Approver cannot edit another agent's listing
```
Given I am logged in as Approver
And I am viewing an Agent's listing
When I look for the "Edit" button
Then the Edit button is not visible
```

### S2: Direct URL access by non-owner
```
Given I am logged in as Agent A
When I navigate to /gio-hang/{Agent-Bs-listing-id}/chinh-sua
Then I see an error or am redirected
```
