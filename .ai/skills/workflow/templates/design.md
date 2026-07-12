# Design: [Feature Name]

> **Date:** [YYYY-MM-DD]
> **Author:** [Name]
> **Status:** Draft / In Review / Approved
> **Requirement:** [Link to requirement document]

---

## Overview

[1-2 sentence summary of what this feature does and why]

---

## Data Model

### New Entities

#### [Entity Name]

```python
class [Entity]Entity(Base):
    __tablename__ = "[table_name]"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Fields here
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Primary key |
| [field] | [type] | [NOT NULL, UNIQUE, etc.] | [Description] |

### Existing Entities to Modify

#### [Entity Name]

| Field to Add | Type | Constraints | Description |
|--------------|------|-------------|-------------|
| [field] | [type] | [NOT NULL, etc.] | [Description] |

### Relationships

```
[Entity A] ──1:N──▶ [Entity B]
[Entity C] ──N:M──▶ [Entity D] (via [junction table])
```

### Database Migrations

- [ ] Create `[table_name]` table
- [ ] Add columns to `[existing_table]`
- [ ] Create indexes: [list indexes]
- [ ] Add foreign keys: [list foreign keys]

---

## API Design

### New Endpoints

#### [Method] [Path]

**Description:** [What this endpoint does]

**RBAC:** [Which roles can access]

**Request:**
```json
{
  "field": "value"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "field": "value"
}
```

**Errors:**
- 400: [Bad request scenario]
- 403: [Forbidden scenario]
- 404: [Not found scenario]
- 409: [Conflict scenario]

### Existing Endpoints to Modify

#### [Method] [Path]

**Changes:**
- [What changes]
- [What changes]

---

## UI Design (if applicable)

### New Pages

#### [Page Name]

**Route:** `/[path]`
**Layout:** [Default / Custom]
**Components:**
- [Component 1]
- [Component 2]

### Existing Pages to Modify

#### [Page Name]

**Changes:**
- [What changes]
- [What changes]

### State Management

| Hook | Type | Purpose |
|------|------|---------|
| `use[Feature]State` | State | [UI state management] |
| `use[Action][Feature]` | Action | [Server mutation] |
| `use[Feature]Mapper` | Mapper | [DTO↔UI transformation] |

---

## Business Rules

### Status Transitions (if applicable)

```
[Status A] ──[action]──▶ [Status B]
[Status A] ──[action]──▶ [Status C]
```

| From | To | Action | RBAC | Side Effects |
|------|----|--------|------|--------------|
| [status] | [status] | [action] | [roles] | [notifications, approvals] |

### Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| [field] | [validation] | [message] |

---

## Cross-Module Impacts

### Notifications

| Event | Recipients | Template |
|-------|------------|----------|
| [event] | [roles] | [template] |

### Approvals (if applicable)

| Action | Approval Required | Approver Role |
|--------|-------------------|---------------|
| [action] | Yes / No | [role] |

### WebSocket (if applicable)

| Event | Payload | Clients |
|-------|---------|---------|
| [event] | [data] | [who receives] |

---

## Documentation Updates

### Files to Update

| File | Changes |
|------|---------|
| `docs/contract/README.md` | [RBAC matrix, new domain, etc.] |
| `docs/contract/<domain>.md` | [New endpoints, business rules] |
| `docs/contract/types.md` | [New enums, schemas] |

### New Business Rules to Document

- [Rule 1]
- [Rule 2]

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [risk] | [High/Medium/Low] | [mitigation] |

---

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]
