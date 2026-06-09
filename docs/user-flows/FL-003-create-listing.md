# Create Listing

## Goal

Agent creates a new property listing in the shared cart.

## Trigger

Agent clicks "Nhập hàng mới" on the homepage.

## Preconditions

- User is logged in as Agent, Approver, or Admin

## Main Flow

```mermaid
flowchart TD
    A[Homepage /] --> B[Click "Nhập hàng mới"]
    B --> C[Create Listing form /gio-hang/tao]
    C --> D[Fill in property attributes]
    D --> E[Upload images]
    E --> F{Save or Submit?}
    F -->|Save as Draft| G[Click "Save"]
    F -->|Submit for Approval| H[Click "Submit for Approval"]
    G --> I[Listing created as DRAFT]
    I --> J[Product Detail page]
    H --> K[Listing created as PENDING_APPROVAL]
    K --> J
```

## Alternative Flows

- **Validation failure**: Show inline errors, stay on form
- **Server error**: Show error toast, preserve form data
- **Cancel**: Navigate away, draft may be auto-saved or discarded

## Screen References

- SC-002 Shared Cart Home
- SC-004 Create Listing

## Story References

- Listing Management US-001 (create listing)
- Business Rules: BR-001, BR-007, BR-008
