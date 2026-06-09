# Hot Products Curation

## Goal

Admin promotes listings to "HOT" status and manages their display order.

## Trigger

Admin navigates to Hot Products from sidebar.

## Preconditions

- User is logged in as Admin

## Main Flow

```mermaid
flowchart TD
    A[Sidebar: Sản phẩm HOT] --> B[Hot Products mgmt /admin/san-pham-hot]
    B --> C{Choose action}
    
    C -->|Add| D[Search for listing]
    D --> E[Select listing to promote]
    E --> F[Listing added to hot list]
    
    C -->|Reorder| G[Drag item to new position]
    G --> H[Order saved]
    
    C -->|Remove| I[Click Remove on hot item]
    I --> J[Confirm]
    J --> K[Listing removed from hot]
    
    C -->|View| L[Browse current hot list]
    L --> M[See 14 hot items max]
    
    F --> N[HOT badge shown on homepage]
    H --> N
    K --> O[HOT badge removed from listing]
```

## Alternative Flows

- **Max limit**: Warn if hot list is full when adding
- **Listing not found**: No results in search

## Screen References

- SC-011 Hot Products Management
- SC-002 Shared Cart Home (HOT badge display)

## Story References

- Hot Products US-001 (promote to hot), US-002 (manage hot list)
