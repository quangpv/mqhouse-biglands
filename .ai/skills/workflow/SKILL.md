---
name: workflow
description: |
  Feature development workflow from customer requirement to deployed code.
  Guides programmer through clarify → explore → design → plan → execute.
  Use when starting a new feature, receiving a customer requirement,
  planning implementation, or when asked to "build a new feature",
  "implement this requirement", "add a new endpoint", "create a new page".
techstack:
  languages:
    - Python 3.10+
    - TypeScript
  frameworks:
    - FastAPI
    - React
  documentation:
    - docs/architecture/
    - docs/contract/
---

# Feature Development Workflow

## Overview

**Never write code before understanding the requirement and having a plan.**

This skill bridges customer requirements to implementation. It guides you through 5 steps: Clarify → Explore → Design → Plan → Execute. Each step produces artifacts that feed the next step and the implementation skills (`backend-dev`, `frontend-dev`, `backend-test`).

### When to Activate

- Starting a new feature from a customer requirement
- Receiving a user story, ticket, or feature request
- Asked to "build X", "implement Y", "add Z"
- Planning implementation before writing code
- When the user says "let's plan this first" or "what do we need to build?"

### When NOT to Activate

- Fixing a bug (use `backend-test` or direct implementation)
- Refactoring existing code (use existing skills)
- Writing tests for existing code (use `backend-test`)
- Quick fixes or typo corrections

---

## The Five Steps

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ CLARIFY │───▶│ EXPLORE │───▶│ DESIGN  │───▶│  PLAN   │───▶│ EXECUTE │
│         │    │         │    │         │    │         │    │         │
│ What?   │    │ Where?  │    │ How?    │    │ Order?  │    │ Build!  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
 requirement.md  codebase map  design.md    impl-plan.md   working code
```

**Duration:** 25-45 minutes total (excluding implementation)

**Output:** Working feature with tests and documentation

---

## Step 1: Clarify (5-10 min)

**Goal:** Understand what the customer wants and why.

**Ask these questions:**

1. "What problem does this solve?" — not "how should it work?"
2. "Who is the user?" — agent, customer, admin, approver?
3. "What should happen when it works?" — happy path
4. "What should happen when it fails?" — error scenarios
5. "Are there business rules?" — constraints, validations, RBAC

**Extract acceptance criteria in Given/When/Then format:**

```markdown
## Acceptance Criteria

### Scenario 1: [Happy path]
**Given** [precondition]
**When** [action]
**Then** [expected outcome]

### Scenario 2: [Error case]
**Given** [precondition]
**When** [action]
**Then** [expected error]

### Scenario 3: [Edge case]
**Given** [precondition]
**When** [action]
**Then** [expected behavior]
```

**Identify business rules:**

- Status transitions (if applicable)
- RBAC restrictions (who can do what)
- Validation rules (required fields, formats, ranges)
- Cross-module impacts (notifications, approvals, WebSocket)

**List edge cases:**

- Empty states (no data yet)
- Boundary values (min/max, first/last)
- Concurrent operations (double submit, race conditions)
- Permission denied scenarios

**Output:** Completed `templates/requirement.md` (saved to `.ai/plans/<feature>-requirement.md`)

---

## Step 2: Explore (5-10 min)

**Goal:** Understand what exists and what needs to change.

### Read Documentation

1. `docs/architecture/README.md` — system overview, tech stack, domain model
2. `docs/architecture/backend.md` — backend patterns, module structure, state machine
3. `docs/architecture/frontend.md` — frontend patterns, routing, data flow
4. `docs/contract/README.md` — global API rules, RBAC matrix, state machine diagram
5. `docs/contract/<relevant-domain>.md` — existing endpoints for the feature area

### Search Codebase

```bash
# Find similar features
grep -r "class.*Repo" backend/src/data/repositories/ --include="*.py" | head -20
grep -r "class.*Facade" backend/src/modules/ --include="*.py" | head -20
grep -r "useQuery\|useMutation" frontend/src/ --include="*.ts" --include="*.tsx" | head -20

# Find existing entities
ls backend/src/data/entities/
ls backend/src/modules/

# Find existing frontend pages
ls frontend/src/pages/
```

### Identify Changes

Ask yourself:

| Question | If YES | If NO |
|----------|--------|-------|
| Is this a new domain? | New module + new entity | — |
| Is this extending an existing domain? | New entity in existing module OR extend existing entity | — |
| Is this a new API? | New endpoint in existing module OR new module | — |
| Is this a new page? | New page under `pages/<feature>/` | — |
| Does this cross modules? | Design cross-module coordination | — |
| Does this need new documentation? | Update `docs/contract/` | — |

**Output:** Codebase map with what exists and what changes (notes for design step)

---

## Step 3: Design (10-15 min)

**Goal:** Define the technical solution before writing code.

### Data Model

- New entities needed? Define fields, types, relationships
- Existing entities to extend? What fields to add?
- Database migrations needed? What changes?
- Indexes for performance? Unique constraints?

### API Design

- New endpoints? Method, path, request/response shapes
- Existing endpoints to modify? What changes?
- RBAC rules? Who can call each endpoint?
- Error responses? Business error messages

### UI Design (if applicable)

- New pages needed? Route, layout, components
- Existing pages to modify? What changes?
- State management? Queries, mutations, cache invalidation
- Form validation? Zod schemas, error display

### Business Rules

- Status transitions? State machine changes?
- Validation rules? Required fields, formats, ranges
- Cross-module impacts? Notifications, approvals, WebSocket
- File upload? Storage, validation, processing

### Documentation Updates

- Which `docs/contract/` files need updating?
- New business rules to document?
- New endpoints to add to API contract?
- RBAC matrix changes?

**Output:** Completed `templates/design.md` (saved to `.ai/plans/<feature>-design.md`)

---

## Step 4: Plan (5-10 min)

**Goal:** Create a step-by-step execution plan.

### Implementation Order

Always follow this order to avoid circular dependencies:

```
1. Data Layer (entities + migrations)
   └─> 2. Repositories (CRUD operations)
       └─> 3. Facades (business logic)
           └─> 4. Router (HTTP endpoints)
               └─> 5. Frontend (DTO → Repository → Query → Facade → View)
                   └─> 6. Tests (unit → integration → E2E)
                       └─> 7. Documentation (docs/contract/ updates)
```

### Files to Create

List every new file with its exact path:

```markdown
## Files to Create

### Backend
- `backend/src/data/entities/<entity>.py` — ORM model
- `backend/src/data/repositories/<entity>_repo.py` — CRUD operations
- `backend/src/modules/<module>/facades/<use_case>.py` — business logic
- `backend/src/modules/<module>/router.py` — HTTP endpoints
- `backend/src/modules/<module>/schemas.py` — Pydantic models
- `backend/src/modules/<module>/mapper.py` — Entity↔Schema conversion

### Frontend
- `frontend/src/data/types/<entity>.dto.ts` — DTO types
- `frontend/src/data/repositories/<entity>Repository.ts` — API calls
- `frontend/src/data/queries/<entity>Queries.ts` — Query key factories
- `frontend/src/pages/<feature>/types.ts` — UI types + Zod schemas
- `frontend/src/pages/<feature>/facades/use<Feature>State.ts` — State hook
- `frontend/src/pages/<feature>/facades/use<Action><Feature>.ts` — Action hook
- `frontend/src/pages/<feature>/facades/use<Feature>Mapper.ts` — Mapper hook
- `frontend/src/pages/<feature>/components/<Component>.tsx` — UI components
- `frontend/src/pages/<feature>/<Feature>Page.tsx` — Page component

### Tests
- `backend/tests/test_<module>/test_<use_case>.py` — Unit tests
- `backend/tests/test_<module>/test_<flow>.py` — Integration tests

### Documentation
- `docs/contract/<domain>.md` — Update or create
- `docs/contract/types.md` — Update if new enums/schemas
- `docs/contract/README.md` — Update if new domain or RBAC changes
```

### Files to Modify

List every existing file that needs changes:

```markdown
## Files to Modify

- `backend/src/main.py` — Register new module
- `backend/src/modules/__init__.py` — Export new module
- `frontend/src/AppRoutes.tsx` — Add new route
- `frontend/src/shared/components/DynamicSidebar.tsx` — Add navigation item
- `docs/contract/README.md` — Update RBAC matrix
```

### Risks and Dependencies

- What could go wrong? (performance, security, data integrity)
- What depends on what? (blocking dependencies)
- What needs special attention? (complex business logic, cross-module coordination)

**Output:** Completed `templates/implementation-plan.md` (saved to `.ai/plans/<feature>-plan.md`)

---

## Step 5: Execute

**Goal:** Implement the feature using the plan and existing skills.

### Delegate to Implementation Skills

| Phase | Skill | What It Receives |
|-------|-------|------------------|
| Backend implementation | `backend-dev` | Implementation plan with file paths and code patterns |
| Frontend implementation | `frontend-dev` | Implementation plan with UI design and data flow |
| Test generation | `backend-test` | Implementation plan with business scenarios and acceptance criteria |

### Execution Order

```bash
# 1. Backend (entities → repos → facades → router)
# Invoke backend-dev skill with implementation plan

# 2. Frontend (DTO → Repository → Query → Facade → View)
# Invoke frontend-dev skill with implementation plan

# 3. Tests (unit → integration → E2E)
# Invoke backend-test skill with implementation plan

# 4. Documentation
# Update docs/contract/ files with new business rules
```

### Documentation Updates

When adding new business rules:

1. **`docs/contract/README.md`** — Update if:
   - Adding new domain/module
   - Changing RBAC matrix
   - Adding new state transitions
   - Changing cross-module interactions

2. **`docs/contract/<domain>.md`** — Update if:
   - Adding new endpoints
   - Changing request/response shapes
   - Adding new business rules
   - Changing status transitions

3. **`docs/contract/types.md`** — Update if:
   - Adding new enums
   - Adding new request/response schemas
   - Changing existing schemas

### Verification Checklist

After implementation, verify:

- [ ] All acceptance criteria from `requirement.md` are met
- [ ] All files from implementation plan are created/modified
- [ ] All tests pass (`pytest`, `npm test`)
- [ ] No layer violations (backend: Router→Facade→Repo, frontend: View→Facade→Data)
- [ ] Documentation updated in `docs/contract/`
- [ ] Business rules documented with examples
- [ ] Error handling covers all edge cases from requirement
- [ ] RBAC rules enforced at router level

---

## Decision Framework

### New Module vs Extend Existing

| Signal | Decision |
|--------|----------|
| New domain (e.g., "invoices", "notifications") | New module |
| Extending existing domain (e.g., "add field to property") | Extend existing module |
| Cross-cutting concern (e.g., "audit log") | New module in `shared/` or `modules/` |

### New Entity vs Extend Existing

| Signal | Decision |
|--------|----------|
| New data type with own lifecycle | New entity |
| Adding fields to existing data | Extend existing entity |
| Junction table for many-to-many | New entity (join table) |
| Lookup/reference data | New entity or extend `meta-data` module |

### New Endpoint vs Modify Existing

| Signal | Decision |
|--------|----------|
| New action on existing resource | New endpoint (e.g., `POST /properties/{id}/approve`) |
| Changing existing behavior | Modify existing endpoint |
| New resource entirely | New CRUD endpoints |

### New Page vs Extend Existing

| Signal | Decision |
|--------|----------|
| New feature with own URL | New page under `pages/<feature>/` |
| Adding UI to existing page | Extend existing page components |
| New tab/section on existing page | New component in existing page |

---

## Templates

Use these templates to structure your outputs:

| Template | When to Use | Location |
|----------|-------------|----------|
| `requirement.md` | Step 1: Capture customer requirement | `.ai/plans/<feature>-requirement.md` |
| `design.md` | Step 3: Technical design document | `.ai/plans/<feature>-design.md` |
| `implementation-plan.md` | Step 4: Step-by-step execution plan | `.ai/plans/<feature>-plan.md` |

All templates are in `.ai/skills/workflow/templates/`.

---

## Quick Reference

### Always

- [ ] Ask "what problem does this solve?" before "how should it work?"
- [ ] Write acceptance criteria in Given/When/Then format
- [ ] Read `docs/architecture/` before designing
- [ ] Read `docs/contract/` before designing API
- [ ] Follow implementation order: entities → repos → facades → router → frontend → tests → docs
- [ ] Update `docs/contract/` when adding new business rules
- [ ] Verify against acceptance criteria after implementation

### Never

- [ ] Write code before having a plan
- [ ] Skip the Clarify step (even if the requirement seems obvious)
- [ ] Design API without reading existing `docs/contract/`
- [ ] Implement frontend before backend is ready
- [ ] Skip documentation updates
- [ ] Deploy without verification checklist

### Key Files

| File | Purpose |
|------|---------|
| `docs/architecture/README.md` | System overview, tech stack, domain model |
| `docs/architecture/backend.md` | Backend patterns, module structure, state machine |
| `docs/architecture/frontend.md` | Frontend patterns, routing, data flow |
| `docs/contract/README.md` | Global API rules, RBAC matrix, state machine |
| `docs/contract/<domain>.md` | Domain-specific endpoints and business rules |
| `.ai/plans/` | Feature planning documents |
| `.ai/skills/backend-dev/SKILL.md` | Backend implementation patterns |
| `.ai/skills/frontend-dev/SKILL.md` | Frontend implementation patterns |
| `.ai/skills/backend-test/SKILL.md` | Test generation patterns |
