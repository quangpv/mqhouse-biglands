# Implementation Plan: [Feature Name]

> **Date:** [YYYY-MM-DD]
> **Author:** [Name]
> **Status:** Ready / In Progress / Complete
> **Requirement:** [Link to requirement document]
> **Design:** [Link to design document]

---

## Overview

[1-2 sentence summary of what will be built]

---

## Implementation Order

```
1. Data Layer (entities + migrations)
   └─> 2. Repositories (CRUD operations)
       └─> 3. Facades (business logic)
           └─> 4. Router (HTTP endpoints)
               └─> 5. Frontend (DTO → Repository → Query → Facade → View)
                   └─> 6. Tests (unit → integration → E2E)
                       └─> 7. Documentation (docs/contract/ updates)
```

---

## Files to Create

### Backend

| # | File Path | Purpose | Dependencies |
|---|-----------|---------|--------------|
| 1 | `backend/src/data/entities/<entity>.py` | ORM model | — |
| 2 | `backend/src/data/repositories/<entity>_repo.py` | CRUD operations | Entity |
| 3 | `backend/src/modules/<module>/schemas.py` | Pydantic models | — |
| 4 | `backend/src/modules/<module>/mapper.py` | Entity↔Schema conversion | Entity, Schemas |
| 5 | `backend/src/modules/<module>/facades/<use_case>.py` | Business logic | Repo, Schemas, Mapper |
| 6 | `backend/src/modules/<module>/router.py` | HTTP endpoints | Facades |

### Frontend

| # | File Path | Purpose | Dependencies |
|---|-----------|---------|--------------|
| 7 | `frontend/src/data/types/<entity>.dto.ts` | DTO types | — |
| 8 | `frontend/src/data/repositories/<entity>Repository.ts` | API calls | DTO |
| 9 | `frontend/src/data/queries/<entity>Queries.ts` | Query key factories | Repository |
| 10 | `frontend/src/pages/<feature>/types.ts` | UI types + Zod schemas | — |
| 11 | `frontend/src/pages/<feature>/facades/use<Feature>State.ts` | State hook | Queries, Mapper |
| 12 | `frontend/src/pages/<feature>/facades/use<Action><Feature>.ts` | Action hook | Repository, Queries |
| 13 | `frontend/src/pages/<feature>/facades/use<Feature>Mapper.ts` | Mapper hook | DTO, UI types |
| 14 | `frontend/src/pages/<feature>/components/<Component>.tsx` | UI components | State, Action hooks |
| 15 | `frontend/src/pages/<feature>/<Feature>Page.tsx` | Page component | Components |

### Tests

| # | File Path | Purpose | Dependencies |
|---|-----------|---------|--------------|
| 16 | `backend/tests/test_<module>/test_<use_case>.py` | Unit tests | Facades |
| 17 | `backend/tests/test_<module>/test_<flow>.py` | Integration tests | Router |

### Documentation

| # | File Path | Purpose | Dependencies |
|---|-----------|---------|--------------|
| 18 | `docs/contract/<domain>.md` | Domain endpoints | Design doc |
| 19 | `docs/contract/types.md` | Enums and schemas | Design doc |
| 20 | `docs/contract/README.md` | Global rules (if needed) | Design doc |

---

## Files to Modify

| # | File Path | Changes | Reason |
|---|-----------|---------|--------|
| 1 | `backend/src/main.py` | Register new module | Module registration |
| 2 | `backend/src/modules/__init__.py` | Export new module | Module export |
| 3 | `backend/src/data/entities/__init__.py` | Export new entity | Entity export |
| 4 | `backend/src/data/repositories/__init__.py` | Export new repo | Repo export |
| 5 | `frontend/src/AppRoutes.tsx` | Add new route | Page routing |
| 6 | `frontend/src/shared/components/DynamicSidebar.tsx` | Add navigation item | Menu entry |

---

## Step-by-Step Instructions

### Phase 1: Data Layer

**Step 1: Create Entity**

```python
# backend/src/data/entities/<entity>.py
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.data.entities._base import Base
import uuid
from datetime import datetime

class [Entity]Entity(Base):
    __tablename__ = "[table_name]"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Add fields from design doc
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
```

**Step 2: Export Entity**

```python
# backend/src/data/entities/__init__.py
from .<entity> import [Entity]Entity
```

**Step 3: Create Migration**

```bash
cd backend
alembic revision --autogenerate -m "add <entity> table"
alembic upgrade head
```

---

### Phase 2: Repositories

**Step 4: Create Repository**

```python
# backend/src/data/repositories/<entity>_repo.py
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.entities import [Entity]Entity
from src.platform.dependencies import get_db

class [Entity]Repo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get(self, id: uuid.UUID) -> [Entity]Entity | None:
        result = await self.db.execute(
            select([Entity]Entity).where([Entity]Entity.id == id)
        )
        return result.scalar_one_or_none()

    async def create(self, entity: [Entity]Entity) -> [Entity]Entity:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
```

**Step 5: Export Repository**

```python
# backend/src/data/repositories/__init__.py
from .<entity>_repo import [Entity]Repo
```

---

### Phase 3: Facades

**Step 6: Create Schemas**

```python
# backend/src/modules/<module>/schemas.py
from pydantic import BaseModel
import uuid
from datetime import datetime

class [Entity]CreateRequest(BaseModel):
    # Fields from design doc

class [Entity]Response(BaseModel):
    id: uuid.UUID
    # Fields from design doc
    created_at: datetime
```

**Step 7: Create Mapper**

```python
# backend/src/modules/<module>/mapper.py
from src.data.entities import [Entity]Entity
from .schemas import [Entity]Response

def [entity]_to_response(entity: [Entity]Entity) -> [Entity]Response:
    return [Entity]Response(
        id=entity.id,
        # Map fields
    )
```

**Step 8: Create Facade**

```python
# backend/src/modules/<module>/facades/<use_case>.py
from fastapi import Depends
from src.data.repositories import [Entity]Repo
from src.modules.<module>.schemas import [Entity]CreateRequest, [Entity]Response
from src.modules.<module>.mapper import [entity]_to_response

async def create_[entity](
    data: [Entity]CreateRequest,
    repo: [Entity]Repo = Depends([Entity]Repo),
) -> [Entity]Response:
    entity = [Entity]Entity(**data.model_dump())
    entity = await repo.create(entity)
    return [entity]_to_response(entity)
```

---

### Phase 4: Router

**Step 9: Create Router**

```python
# backend/src/modules/<module>/router.py
from fastapi import APIRouter, Depends, status
from src.modules.<module>.facades.<use_case> import create_[entity]
from src.modules.<module>.schemas import [Entity]CreateRequest, [Entity]Response

def module():
    router = APIRouter(prefix="/<route>", tags=["<tag>"])

    @router.post("/", response_model=[Entity]Response, status_code=status.HTTP_201_CREATED)
    async def create_endpoint(result: [Entity]Response = Depends(create_[entity])):
        return result

    return router
```

**Step 10: Register Module**

```python
# backend/src/main.py
from src.modules.<module>.router import module as <module>_module

MODULES = [
    # ... existing modules
    <module>_module,
]
```

---

### Phase 5: Frontend

**Step 11: Create DTO**

```typescript
// frontend/src/data/types/<entity>.dto.ts
export interface [Entity]DTO {
  id: string;
  // Fields from design doc
  created_at: string;
}
```

**Step 12: Create Repository**

```typescript
// frontend/src/data/repositories/<entity>Repository.ts
import { httpClient } from "@/platform/http/client";
import { [Entity]DTO } from "@/data/types/<entity>.dto";

export const [entity]Repository = {
  get: async (id: string): Promise<[Entity]DTO> => {
    return httpClient.get(`/<route>/${id}`);
  },

  create: async (data: Create[Entity]Payload): Promise<[Entity]DTO> => {
    return httpClient.post("/<route>", data);
  },
};
```

**Step 13: Create Query Keys**

```typescript
// frontend/src/data/queries/<entity>Queries.ts
export const [entity]Queries = {
  all: ["[entity]"] as const,
  detail: (id: string) => [...[entity]Queries.all, id] as const,
};
```

**Step 14-17: Create Frontend Facades and Components**

Follow the `frontend-dev` skill patterns for:
- `types.ts` — Zod schemas + UI types
- `use<Feature>State.ts` — State hook
- `use<Action><Feature>.ts` — Action hook
- `use<Feature>Mapper.ts` — Mapper hook
- Components and Page

---

### Phase 6: Tests

**Step 18: Create Unit Tests**

Follow the `backend-test` skill patterns for:
- Business-language test names
- Exhaustive role × status matrix
- Mock repos, assert business outcomes

**Step 19: Create Integration Tests**

Follow the `backend-test` skill patterns for:
- Real DB operations
- Multi-step flows
- Auth middleware verification

---

### Phase 7: Documentation

**Step 20: Update Documentation**

Update `docs/contract/` files with:
- New endpoints
- Business rules
- RBAC changes
- Status transitions

---

## Verification Checklist

### Backend

- [ ] Entity follows coding standards (UUID PK, timestamps, Mapped types)
- [ ] Repository has CRUD methods with proper typing
- [ ] Facade has one function per use case
- [ ] Router delegates to facades via Depends()
- [ ] All dependencies wired via DI
- [ ] Error handling uses typed exceptions

### Frontend

- [ ] DTO types match API response
- [ ] Repository returns DTOs only
- [ ] Query keys follow factory pattern
- [ ] State hook manages UI state
- [ ] Action hook handles mutations
- [ ] Mapper converts DTO↔UI types
- [ ] View uses facade hooks only
- [ ] No layer violations

### Tests

- [ ] Unit tests have business-language names
- [ ] Integration tests use real DB
- [ ] All roles × statuses covered
- [ ] Error scenarios tested
- [ ] All tests pass

### Documentation

- [ ] `docs/contract/` updated
- [ ] Business rules documented
- [ ] RBAC matrix updated
- [ ] Examples provided

---

## Risks and Mitigations

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| [risk] | [High/Medium/Low] | [mitigation] | [Open/Resolved] |

---

## Progress

| Phase | Status | Notes |
|-------|--------|-------|
| 1. Data Layer | ⬜ Not Started | |
| 2. Repositories | ⬜ Not Started | |
| 3. Facades | ⬜ Not Started | |
| 4. Router | ⬜ Not Started | |
| 5. Frontend | ⬜ Not Started | |
| 6. Tests | ⬜ Not Started | |
| 7. Documentation | ⬜ Not Started | |
