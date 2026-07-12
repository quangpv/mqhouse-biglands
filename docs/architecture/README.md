# Architecture

System architecture documentation for Biglands — a Vietnamese real estate (BDS) platform.

## System Overview

Biglands manages property listings through their full lifecycle: draft → approval → listing → deposit → sale/completion. It supports multi-role workflows (SALE agents, APPROVERs, ADMINs) with organization-based access control, real-time notifications, and Vietnamese-localized search.

### Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19 + TypeScript, Vite 8, TanStack Query v5, Zustand v5, Axios, React Hook Form + Zod, Tailwind CSS v4 + shadcn/ui |
| **Backend** | Python 3.13, FastAPI, SQLAlchemy 2.0 (async), asyncpg, Alembic |
| **Database** | PostgreSQL 16 |
| **Real-time** | WebSocket (FastAPI native) |
| **Background Jobs** | APScheduler (property expiration, file cleanup) |
| **Deployment** | Docker Compose, GHCR images |

### Architecture Principles

1. **Modular** — Backend feature modules with consistent structure (router + facades + schemas + mapper). Frontend features self-contained under `pages/<feature>/`.
2. **Facade Pattern** — Each use case is a standalone async function acting as the route handler (backend) or action hook (frontend).
3. **State Machine** — Property lifecycle with 13 states, 7 transitions, and approval workflow.
4. **Async-First** — Entire backend stack is async (SQLAlchemy async, asyncpg, async session management).
5. **Protocol-Based Abstraction** — FileStorage, EmailService use protocols for swappable implementations.

## Document Map

| Document | Scope | Key Topics |
|---|---|---|
| [frontend.md](./frontend.md) | Frontend architecture | React patterns, View→Facade→Data→Platform layers, auth, routing, shared hooks, WebSocket |
| [backend.md](./backend.md) | Backend architecture | FastAPI modules, DI container, repository pattern, state machine, data layer, deployment |

## Domain Model

```
Users ──belong_to──> Organizations
  │
  ├──create──> Properties ──have──> Transitions (audit trail)
  │               │
  │               ├──request──> Approvals ──decide──> Properties
  │               │
  │               ├──have──> Tags, Transaction Types, Property Types
  │               ├──have──> Images, Certificates (Files)
  │               ├──have──> Reviews ──have──> Images (Files)
  │               ├──have──> Pins (per user)
  │               └──can_be──> Hot Properties (admin-managed)
  │
  └──receive──> Notifications ──delivered_via──> WebSocket

Files ──optimized_to──> WebP + Thumbnails
       ──trashed_on_delete──> Cleanup (30-day retention)

Scheduled Jobs:
  - Property expiration (daily cron)
  - File orphan cleanup (24h interval)
```

## API Documentation

See [docs/api-contract/](../api-contract/) for complete API business rules organized by domain.
