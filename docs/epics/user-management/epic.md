# Epic: User Management

## Business Goal

Allow admins to manage who can access the platform and what permissions they
have.

## Problem Statement

Access to the platform should be controlled and role-appropriate. New agents
need accounts, departing agents need deactivation, and role changes need to
be reflected immediately.

## Business Value

- Security: only authorized agents can access the deal pool
- Accountability: all actions are traceable to a named user
- Scalability: easy onboarding of new agents

## Actors

- Admin

## Scope

### In Scope

- Create user (name, username, phone, role)
- Edit user profile
- Deactivate/reactivate user
- Assign/change user role
- List all users with search

### Out of Scope

- Self-registration
- SSO integration
- User deletion (soft-deactivate only)

## Features

- User CRUD
- Role assignment
- Active/inactive toggle
- User list with search

## Dependencies

- None

## Business Rules

- Users cannot delete themselves.
- At least one ADMIN must always exist.
- Deactivated users cannot log in.
