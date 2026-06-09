# Epic: Deposit & Deal Lifecycle

## Business Goal

Digitize the cash deposit and deal closure process so agents and approvers can
track deal progress in real time.

## Problem Statement

Deposit and deal closure were previously handled via verbal confirmation or
offline payments, causing disputes over who deposited first or whether a deal
was actually closed.

## Business Value

- Clear first-depositor priority prevents agent disputes
- Real-time deal status eliminates guesswork
- Digital audit trail for commission reconciliation

## Actors

- Agent (reports deposit, closure, cancellation, sold-out)
- Approver (confirms each event)

## Scope

### In Scope

- Report customer deposit with name, phone, amount
- Approve/reject deposit report
- Report deal closure (after deposit confirmed)
- Approve/reject deal closure
- Report deposit cancellation with reason
- Approve/reject cancellation
- Report listing as sold-out
- Approve/reject sold-out
- Status transitions: ACTIVE → DEPOSITED → CLOSED / CANCELLED → SOLD_OUT

### Out of Scope

- Payment processing (deposit is offline)
- Commission payout automation
- Contract/document attachment

## Features

- Report deposit form (customer name, phone, amount)
- Approve deposit in approval queue
- Report deal closure (only after deposit confirmed)
- Report cancellation with reason
- Sold-out report
- Status badge visible on listing card

## Dependencies

- Approval Workflow
- Listing Management

## Business Rules

- BR-001 Only one active deposit per listing.
- BR-002 Deal closure requires a confirmed deposit.
- BR-003 Cancellation requires a confirmed deposit.
- BR-004 Only the listing creator can report these events.
- BR-005 Only approver can confirm these events.
