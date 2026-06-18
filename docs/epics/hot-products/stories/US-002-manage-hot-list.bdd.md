# BDD: Manage Hot Products List

> **Story**: US-002-manage-hot-list
> **Priority**: Should Have
> **Related**: Listing entity, HP-003, HP-004

## Acceptance Criteria
- Admin can view all hot products in one place
- Admin can remove items from hot list
- Admin can reorder hot items via drag-and-drop

## Happy Paths

### H1: View hot products list
```
Given I am logged in as Admin
And at least one listing is marked as Hot
When I navigate to the Hot Products management page
Then I see a list of all listings with "Hot" status
And each listing shows title, image, and current position
```

### H2: Remove listing from hot list
```
Given I am viewing the hot products list
When I click "Remove" on a listing
And I confirm
Then the listing is no longer hot
And the listing is removed from the hot list display
And the "🔥 HOT" badge disappears from the listing card
```

### H3: Reorder hot listings
```
Given I am viewing the hot products list
When I drag a listing to a new position
Then the order is saved
And the new order is reflected on the homepage
```

### H4: Empty hot list state
```
Given no listings are marked as Hot
When I navigate to the Hot Products management page
Then I see an empty state message indicating no hot products
And I can search to add new ones
```

## Error Cases

### E1: Search no results when adding
```
Given I am on the add-hot-product search
When I search for a non-existent listing
Then I see "No results found"
```

## Edge Cases

### EC1: Reorder with single item
```
Given there is only 1 hot listing
When I attempt to drag it
Then reordering has no practical effect
And no error occurs
```

### EC2: Remove all hot items
```
Given there are multiple hot items
When I remove all of them one by one
Then the hot products list shows empty
And the homepage hot section is hidden
```

### EC3: Rapid reordering
```
Given there are 14 hot items
When I reorder multiple items in rapid succession
Then each reorder is persisted correctly
And the final order matches my actions
```

## Security Cases

### S1: Agent accesses hot management route
```
Given I am logged in as Agent
When I navigate to /admin/san-pham-hot
Then I see "Bạn không có quyền truy cập trang này"
```

### S2: Unauthenticated access
```
Given I am not logged in
When I attempt to access /admin/san-pham-hot
Then I am redirected to the login page
```
