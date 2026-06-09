# Report Deposit

## Goal

Agent reports that a customer has placed a deposit on a listing.

## Trigger

Agent clicks "Báo cọc" on the Product Detail page.

## Preconditions

- User is logged in as the listing owner
- Listing status is ACTIVE
- No active deposit exists on this listing (BR-001)

## Main Flow

```mermaid
flowchart TD
    A[Product Detail] --> B[Click "Báo cọc"]
    B --> C[Deposit form dialog]
    C --> D[Enter: customer name, phone, deposit amount, notes]
    D --> E[Submit]
    E --> F[DealEvent created: DEPOSIT_REPORTED]
    F --> G[Status unchanged (pending approval)]
    G --> H[Notification sent to approvers]
```

## Alternative Flows

- **Validation**: Customer name and deposit amount required
- **Duplicate deposit**: Error if deposit already reported and pending
- **Cancel**: Close dialog, no changes

## Screen References

- SC-003 Product Detail

## Story References

- Deposit/Deal Lifecycle US-001 (report deposit)
