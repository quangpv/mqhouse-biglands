# Cancellation Pipeline

## Goal

Agent reports deposit cancellation; approver confirms.

## Trigger

Agent clicks "Báo huỷ cọc" on Product Detail.

## Preconditions

- User is logged in as the listing owner
- Listing status is DEPOSITED (deposit confirmed)

## Main Flow

```mermaid
flowchart TD
    A[Product Detail] --> B[Click "Báo huỷ cọc"]
    B --> C[Cancellation form: reason, notes]
    C --> D[DealEvent: CANCELLATION_REPORTED]
    D --> E[Notification sent to approvers]
    E --> F[Approver queue: Duyệt huỷ cọc]
    F --> G{Approve?}
    G -->|Yes| H[DealEvent: CANCELLATION_CONFIRMED]
    H --> I[Listing status → CANCELLED]
    G -->|No| J[Reject with reason]
    J --> K[Listing stays DEPOSITED]
```

## Alternative Flows

- **Reject**: Listing remains DEPOSITED
- **Re-list**: After cancellation, agent can re-submit listing (→ ACTIVE)

## Screen References

- SC-003 Product Detail
- SC-008 Approval Queue

## Story References

- Deposit/Deal Lifecycle US-004 (report cancellation), US-005 (approve cancellation)
