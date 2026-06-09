# Browse & Discover

## Goal

Agent browses available listings, filters by type, searches, pins favorites, and navigates to product detail.

## Trigger

User logs in and lands on homepage.

## Preconditions

- User is authenticated

## Main Flow

```mermaid
flowchart TD
    A[Homepage /] --> B{Choose action}
    B -->|Browse grid| C[Scroll paginated listings]
    B -->|Search| D[Type keyword in search box]
    B -->|Filter tab| E[Click filter tab]
    B -->|View detail| F[Click listing card]
    
    D --> G[Results update in real-time]
    E --> H[Switch to All / Pinned / Hot]
    C --> B
    G --> B
    H --> B
    
    F --> I[Product Detail /san-pham/:id]
    I --> J{Perform deal action}
    J -->|Back to grid| B
```

## Alternative Flows

- **Empty results**: Show empty state message with search term
- **No listings**: Show empty state
- **Pin**: User can pin listings for quick access via "Đã ghim" filter

## Screen References

- SC-002 Shared Cart Home
- SC-003 Product Detail

## Story References

- Shared Cart Browsing US-001 (browse), US-002 (search), US-003 (filter), US-004 (view detail), US-005 (pin)
