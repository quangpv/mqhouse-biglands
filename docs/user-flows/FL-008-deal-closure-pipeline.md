# Deal Closure Pipeline

## Goal

Agent reports deal closure; approver confirms.

## Trigger

Agent clicks "Báo chốt hàng" on Product Detail.

## Preconditions

- User is logged in as the listing owner
- Listing status is DEPOSITED (deposit confirmed)

## Main Flow

```mermaid
flowchart TD
    A[Product Detail] --> B[Click "Báo chốt hàng"]
    B --> C[Closure form: notes]
    C --> D[DealEvent: CLOSURE_REPORTED]
    D --> E[Notification sent to approvers]
    E --> F[Approver queue: Duyệt chốt hàng]
    F --> G{Approve?}
    G -->|Yes| H[DealEvent: CLOSURE_CONFIRMED]
    H --> I[Listing status → CLOSED]
    G -->|No| J[Reject with reason]
    J --> K[Listing stays DEPOSITED]
```

## Alternative Flows

- **Reject**: Listing remains DEPOSITED; agent can retry

## Screen References

- SC-003 Product Detail
- SC-008 Approval Queue

## Story References

- Deposit/Deal Lifecycle US-003 (report deal closure)
