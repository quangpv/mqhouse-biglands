# Story: View Product Detail

## User Story

As an Agent
I want to view the full details of a listing
So that I can evaluate the property and share information with customers

## Description

The product detail page shows an image gallery, full property attributes,
description text, agent contact info, and deal action buttons.

## Preconditions

- User is logged in
- Listing exists and is in ACTIVE or DEPOSITED status

## Acceptance Criteria

### Happy Path

Given I am browsing listings
When I click on a listing card
Then I navigate to the product detail page
And I see the image gallery with navigation
And I see all property attributes (price, area, rooms, etc.)
And I see the full description
And I see the agent name and date
And I see action buttons (Report Deposit, Report Sold-Out, etc.)

## Business Rules

- Listing detail page is viewable by all authenticated users regardless of role

## Related Entities

- Listing
- ListingImage

## Priority

Must Have
