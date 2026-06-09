# Epic: Listing Management

## Business Goal

Enable agents to create, edit, and manage their property listings.

## Problem Statement

Agents need a structured way to input property data beyond unstructured text
messages. The platform must ensure all required listing data is captured
consistently.

## Business Value

- Standardized property data improves search and discovery
- Reduces back-and-forth between agents and approvers
- Enables data-driven decisions (price per m² comparisons, etc.)

## Actors

- Agent (creates and edits)
- Approver (reviews post-submission)

## Scope

### In Scope

- Create listing with full property attributes
- Upload images (up to N images)
- Auto-generate product code
- Edit own listings (before or after approval)
- Change listing status with reason
- Delete draft listings

### Out of Scope

- Template-based listing creation
- Bulk CSV import

## Features

- Listing creation form with all property fields
- Image upload with reorder and primary image selection
- Auto-generated product code
- Draft save before submission
- Edit existing listings (status-dependent)
- Delete listing (draft only)

## Dependencies

- User must exist and be active
- Image storage service must be available

## Business Rules

- BR-001 Listing code is auto-generated based on date and sequence.
- BR-006 Rejected listings return to DRAFT for editing.
- BR-007 At least one image is required before submission for approval.
- BR-008 Commission is required for SANG_NHUONG and BAN transaction types.
