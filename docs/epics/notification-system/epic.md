# Epic: Notification System

## Business Goal

Keep agents and approvers informed of important events without relying on
external channels.

## Problem Statement

Agents miss critical updates (approval decisions, deposit confirmations) when
they are only communicated via the listing page. Approvers miss pending tasks.

## Business Value

- Faster response times on approvals
- Agents know immediately when their listing is approved or rejected
- Reduces need for Zalo/phone follow-ups

## Actors

- All authenticated users

## Scope

### In Scope

- Receive notification when listing is approved/rejected
- Receive notification when deposit is reported/confirmed
- Receive notification when deal is closed
- Notification list page
- Unread count badge in navigation
- Mark as read

### Out of Scope

- Push notifications
- Email/SMS notifications
- Notification preferences

## Features

- In-app notification list
- Unread badge counter
- Notification types: listing approved, deposit reported, deal closed, etc.
- Mark single/all as read

## Dependencies

- All other epics (events trigger notifications)

## Business Rules

- BR-010 Notifications are role-scoped: agents see relevant notifications; admins see all system-wide notifications.
