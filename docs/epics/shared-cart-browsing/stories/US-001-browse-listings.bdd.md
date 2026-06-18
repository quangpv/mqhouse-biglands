# BDD: Browse Listings

> **Story**: US-001-browse-listings
> **Priority**: Must Have
> **Related**: Listing, BR-009, BR-015, LV-001, LV-002, LV-004

## Acceptance Criteria
- Authenticated users see a paginated grid of listing cards
- Listings sorted by recency
- Total count displayed
- Hot listings appear in dedicated section first
- Terminal-status listings are hidden

## Happy Paths

### H1: Browse shared cart as Agent
```
Given I am logged in as an Agent
When I navigate to the homepage
Then I see a grid of listing cards sorted by recency
And I see the total count of listings displayed
And each card shows: title, price, commission, address, area, rooms, bathrooms, floors, agent name, date, thumbnail
And I can scroll through pages using pagination
```

### H2: Browse as Approver
```
Given I am logged in as Approver
When I navigate to the homepage
Then I see the same listing grid as agents
```

### H3: Browse as Admin
```
Given I am logged in as Admin
When I navigate to the homepage
Then I see the listing grid
And I see approval queue counts in the sidebar
```

### H4: Pagination navigation
```
Given I am on the homepage
When I click "Next"
Then I see the next page of listings
When I click a page number "3"
Then I jump to page 3
```

### H5: Hot listings section
```
Given there are listings marked as Hot
When I view the homepage
Then I see a horizontal scrollable "Sản phẩm Hot" section above the filter tabs
And hot listings appear first in the grid with a "🔥 HOT" badge
```

## Error Cases

### E1: Empty shared cart
```
Given there are 0 active listings
When I view the homepage
Then I see an empty state message
```

## Security Cases

### S1: Unauthenticated user redirected
```
Given I am not logged in
When I navigate to the homepage
Then I am redirected to the login page
```

### S2: Unauthenticated API access
```
Given I have no session
When I send a GET request to the listings API
Then the response is HTTP 401 Unauthorized
```
