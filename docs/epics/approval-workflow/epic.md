# Epic: Approval Workflow

## Business Goal

Ensure all listings, deposits, deal closures, cancellations, and sold-out
reports are verified by a designated approver before taking effect.

## Problem Statement

Without a moderation layer, agents could publish inaccurate information, report
false deposits, or close deals without verification. This erodes trust in the
shared deal pool.

## Business Value

- Data integrity of the shared cart
- Fraud prevention (false deposits, fake closures)
- Clear audit trail for all listing lifecycle changes
- Accountability for both agents and approvers

## Actors

- Agent (reports events)
- Approver (confirms or rejects events)

## Scope

### In Scope

- 15 approval queues (3 transaction types × 5 stages)
- Approve or reject with reason
- Badge count of pending items per queue
- Rejection returns the listing to previous status with reason
- Audit log of all approval decisions

### Out of Scope

- Tiered approval (multiple approvers)
- Scheduled auto-approval
- SLA tracking

## Features

- Approval queue pages per transaction type and stage
- Approve/reject action with required reason on rejection
- Pending count badges in navigation
- Listing detail within approval context
- Filter pending/approved/rejected in queue

## Dependencies

- Listing Management
- Deposit & Deal Lifecycle

## Business Rules

- BR-005 Only APPROVER or ADMIN roles can confirm decisions.
- BR-006 Rejection must include a reason.
- BR-001 Listing must be in the correct status for each approval stage.
