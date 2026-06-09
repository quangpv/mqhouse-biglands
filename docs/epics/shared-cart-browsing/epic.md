# Epic: Shared Cart Browsing

## Business Goal

Enable agents to quickly discover and evaluate CHDV properties from a unified
shared deal pool.

## Problem Statement

Agents previously relied on fragmented Zalo groups and spreadsheets to find
available properties. There was no single source of truth for what was on the
market, its status, or key attributes.

## Business Value

- Reduces time to find viable properties from hours to minutes
- Eliminates duplicate efforts from agents unknowingly marketing the same property
- Gives all agents equal access to the deal pool

## Actors

- Agent (primary)
- Unauthenticated viewer (limited)

## Scope

### In Scope

- View paginated listing grid
- Search by keyword (product code, title, content, address)
- Filter by All/Pinned/Hot categories
- View product detail page with gallery and full attributes
- Pagination (Previous/Next + page numbers)
- Pin/unpin listings to personal watchlist

### Out of Scope

- Advanced multi-faceted search (by price range, district, etc.)
- Map-based browsing

## Features

- Paginated product card grid
- Keyword search across title, code, address, content
- Category filter tabs: All / Pinned / Hot
- Product detail page with image gallery
- Pin/unpin toggle on listing cards
- Responsive card layout showing key attributes at a glance

## Dependencies

- Listing data must be indexed and searchable

## Business Rules

- BR-001 Listings with status ACTIVE, DEPOSITED are visible in shared cart.
- BR-002 SOLD_OUT and CANCELLED listings are hidden from shared cart.
- BR-003 Hot listings appear first with a visual badge.
- BR-004 Pinning is a per-user preference, not a global state.
