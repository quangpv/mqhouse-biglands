# Edit Listing

## Goal

Agent modifies an existing listing's attributes.

## Trigger

Agent clicks "Edit" on their own listing (from My Cart or Product Detail).

## Preconditions

- User is logged in as the listing owner
- Listing exists and is editable (status-dependent)

## Main Flow

```mermaid
flowchart TD
    A[Product Detail or My Cart] --> B[Click Edit]
    B --> C[Edit form pre-filled /gio-hang/:id/chinh-sua]
    C --> D[Modify fields]
    D --> E[Save changes]
    E --> F[Listing updated]
    F --> G[Product Detail page]
```

## Alternative Flows

- **Listing already approved**: Editing may require re-submission for approval
- **Draft listing**: Save without re-submission
- **Validation failure**: Show inline errors, stay on form

## Screen References

- SC-005 Edit Listing
- SC-003 Product Detail
- SC-006 My Cart

## Story References

- Listing Management US-002 (edit listing)
