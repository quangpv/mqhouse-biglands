# BDD: Filter Listings by Category

> **Story**: US-003-filter-listings
> **Priority**: Should Have
> **Related**: Listing, LV-003

## Acceptance Criteria
- Three filter tabs: All / Pinned / Hot
- Each tab shows the count of matching listings
- Empty state shown when filter yields no results

## Happy Paths

### H1: Filter by Hot
```
Given I am on the shared cart page
When I click the "Hàng Hot" tab
Then I see only listings marked as Hot
And the tab shows the count of hot listings
```

### H2: Filter by Pinned
```
Given I have pinned several listings
When I click the "Đã ghim" tab
Then I see only listings I have pinned
And the tab shows the count of my pinned listings
```

### H3: Switch back to All
```
Given I am viewing the Hot filter
When I click the "Tất cả loại hàng" tab
Then I see all active listings again
```

## Error Cases

### E1: No pinned listings
```
Given I have not pinned any listings
When I switch to the "Đã ghim" tab
Then I see an empty state message
```

### E2: No hot listings
```
Given no listings are marked as Hot
When I switch to the "Hàng Hot" tab
Then I see an empty state message
```

## Edge Cases

### EC1: Filter combined with search
```
Given I am viewing the "Đã ghim" tab
When I type a search term
Then search results are scoped to my pinned listings only
```

### EC2: Pin a listing while viewing All
```
Given I am viewing the "Tất cả loại hàng" tab
When I pin a listing
Then the pin icon updates
And the "Đã ghim" tab count increases
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I attempt to access the shared cart
Then I am redirected to the login page
```
