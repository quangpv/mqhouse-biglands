# BDD: Pin/Unpin Listings

> **Story**: US-005-pin-listings
> **Priority**: Should Have
> **Related**: Listing, UserPin (proposed), LV-003

## Acceptance Criteria
- Any authenticated user can pin/unpin any listing
- Pin is per-user (not global)
- Pin icon visually indicates state
- Pinned listings appear in "Đã ghim" filter tab

## Happy Paths

### H1: Pin a listing
```
Given I am logged in as an Agent
And I am viewing a listing card
When I click the pin button
Then the listing is added to my pinned list
And the pin icon changes to the pinned state
```

### H2: Unpin a listing
```
Given I have pinned a listing
When I click the pinned button again
Then the listing is removed from my pinned list
And the pin icon returns to the unpinned state
```

### H3: Pinned listing appears in filter
```
Given I have pinned a listing
When I navigate to the shared cart
And I click the "Đã ghim" tab
Then I see the pinned listing in the filtered results
```

## Edge Cases

### EC1: Pin listing from product detail
```
Given I am viewing a product detail page
When I click the pin/favourite icon
Then the listing is pinned
```

### EC2: Unpin a listing that is no longer active
```
Given I have pinned a listing that later becomes SOLD_OUT
When I view my pinned list
Then the listing may appear or not based on visibility rules
```

### EC3: Pin same listing twice
```
Given I have already pinned a listing
When I click the pin button again
Then the listing is unpinned (toggle)
```

### EC4: Multiple users pin the same listing
```
Given Agent A and Agent B both view the same listing
When Agent A pins the listing
And Agent B pins the listing
Then both agents see the listing in their respective pinned lists
And the pin is independent per user
```

## Security Cases

### S1: Unauthenticated user
```
Given I am not logged in
When I attempt to pin a listing
Then the pin button is not visible or redirects to login
```
