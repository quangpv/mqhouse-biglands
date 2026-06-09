# Sold-Out Pipeline

## Goal

Agent reports listing as sold-out (direct sale, no deposit); approver confirms.

## Trigger

Agent clicks "Báo hết hàng" on Product Detail.

## Preconditions

- User is logged in as the listing owner
- Listing status is ACTIVE

## Main Flow

```mermaid
flowchart TD
    A[Product Detail] --> B[Click "Báo hết hàng"]
    B --> C[Sold-out form: notes]
    C --> D[DealEvent: SOLD_OUT_REPORTED]
    D --> E[Notification sent to approvers]
    E --> F[Approver queue: Duyệt hết hàng]
    F --> G{Approve?}
    G -->|Yes| H[DealEvent: SOLD_OUT_CONFIRMED]
    H --> I[Listing status → SOLD_OUT]
    G -->|No| J[Reject with reason]
    J --> K[Listing stays ACTIVE]
```

## Alternative Flows

- **Reject**: Listing remains ACTIVE

## Screen References

- SC-003 Product Detail
- SC-008 Approval Queue

## Story References

- Deposit/Deal Lifecycle US-006 (mark sold-out)
