# BDD: Search Listings

> **Story**: US-002-search-listings
> **Priority**: Must Have
> **Related**: Listing

## Acceptance Criteria
- Search across product code, title, description, address, ward, district
- Results update in real-time as user types
- Empty results show message with search term
- Special characters handled safely

## Happy Paths

### H1: Search by product code
```
Given I am on the shared cart page
When I type a product code "250520" into the search box
Then the listing grid updates to show only listings with matching product code
And the result count updates accordingly
```

### H2: Search by title keyword
```
Given I am on the shared cart page
When I type "CHDV Quận 1" into the search box
Then the listing grid shows listings with matching title or description
```

### H3: Search by address
```
Given I am on the shared cart page
When I type "Nguyễn Huệ" into the search box
Then I see listings with matching address
```

## Error Cases

### E1: No matching results
```
Given I am on the shared cart page
When I type a search term that matches nothing
Then I see an empty results message: "No results found for '[search term]'"
```

### E2: Special characters in search
```
Given I am on the shared cart page
When I type special characters like "<script>" into the search box
Then the search is executed safely without errors
And no results are unexpectedly returned
```

## Security Cases

### S1: SQL injection attempt
```
Given I am on the shared cart page
When I type "' OR 1=1 --" into the search box
Then the search is sanitized
And no unauthorized data is exposed
```

### S2: XSS attempt through search
```
Given I am on the shared cart page
When I type a script tag into the search
Then the input is sanitized
And no script execution occurs
```
