---
name: backend-test
description: "Automated backend test generation with business-language naming. Reads facade/module code, generates exhaustive test matrices, writes unit/integration/E2E tests. Use when writing new features, fixing bugs with no coverage, or pre-PR."
origin: ECC
techstack:
  languages: [python]
  frameworks: [fastapi, pytest, sqlalchemy]
---

# Backend Test Generation

**Write tests from a business perspective, not a technical perspective.**

Test names must be written in business language that a product owner or customer can understand. Each test should describe a business outcome, not a technical action.

---

## The One Rule

> **If a product owner wouldn't understand the test name from reading it, rename it.**

Every test answers a business question:
- "Can an agent create a property draft?"
- "Does the system prevent double approvals?"
- "What happens when a deposit expires?"

No test answers a technical question:
- "Does POST /properties return 201?"
- "Does the status field update correctly?"
- "Does the mock repository get called?"

---

## What Business-Language Means

| ❌ Technical (don't do this) | ✅ Business (do this) |
|---|---|
| `test_create_property_201` | `test_agent_creates_property_draft` |
| `test_post_endpoint_returns_success` | `test_customer_makes_deposit_on_property` |
| `test_property_status_update` | `test_system_advances_property_through_lifecycle` |
| `test_put_returns_403` | `test_sale_cannot_edit_other_agents_property` |
| `test_delete_removes_record` | `test_admin_removes_unlisted_property` |
| `test_approve_sets_status` | `test_approver_confirms_property_listing` |
| `test_transition_409_conflict` | `test_system_prevents_double_approval` |
| `test_auth_401_unauthorized` | `test_unauthenticated_user_cannot_create_property` |
| `test_login_with_wrong_password` | `test_wrong_password_returns_generic_error` |
| `test_pagination_page_2` | `test_second_page_of_results_returns_correct_properties` |
| `test_filter_by_price_range` | `test_buyer_finds_properties_within_budget` |
| `test_search_returns_results` | `test_agent_searches_by_address_finds_matching_properties` |
| `test_file_upload_validates_type` | `test_system_rejects_non_image_files` |
| `test_expire_deposited_property` | `test_system_expires_overdue_deposit_automatically` |
| `test_websocket_sends_notification` | `test_agent_receives_real_time_approval_notification` |

**The pattern:** `test_{actor}_{action}_{expected_outcome}`

- **Actor:** who does it (agent, customer, admin, approver, system)
- **Action:** what they do (creates, submits, approves, searches)
- **Outcome:** what happens (draft created, approval pending, property available)

---

## When to Activate

- Writing new features (new facade, new endpoint, new module)
- Fixing bugs with no existing test coverage
- Pre-PR verification (missing tests for changed code)
- Refactoring facades (need to verify behavior preserved)
- Adding new status transitions or business rules

---

## Automated Workflow

### Step 1: Analyze — Business Scenarios, Not Code Paths

Read the target module/facade files. Ask:

> **"What business scenarios does this code enable?"**

Output a list of business scenarios, not code branches.

**Wrong approach (code-centric):**
```
POST /properties with is_draft=true → 201
POST /properties with is_draft=false + SALE role → creates approval
PUT /properties/{id} with status=available + SALE role → changes to edit_pending
```

**Right approach (business-centric):**
```
Agent creates a property draft
Agent publishes a property for approval
Agent edits a listed property (requires re-approval)
Admin edits a listed property (applied immediately)
Agent submits draft for approval
Agent withdraws a pending request
Customer makes a deposit on a property
Agent reports a property as sold
```

**How to extract business scenarios:**
1. Read every facade function — each is a business use case
2. Read the status/state machine — each transition is a business scenario
3. Read the RBAC rules — each role restriction is a test scenario
4. Read error handlers — each error code maps to a business guard

---

### Step 2: Classify — Business Risk, Not Code Architecture

Ask:

> **"What happens if this logic breaks?"**

| Risk Level | What Breaks | Test Level |
|---|---|---|
| **High** — financial data or workflow | Money, contracts, legal state | Unit (exhaustive) + Integration |
| **Medium** — user-facing behavior | Search, filters, pagination, UX | Integration (real DB) |
| **Low** — cross-module coordination | Notifications, side effects | Integration (multi-step) |
| **Critical** — blocks entire journey | Core workflow (create→approve→list) | E2E (≤10 total) |
| **Trivial** — simple CRUD, no branching | Tags, Property Types, Organizations | Skip unit, keep existing integration |

**Decision flowchart:**

```
Is there branching logic (if/else based on role, status, or input)?
  → YES: Unit test (exhaustive matrix)
  → NO ↓

Does it touch real SQL (WHERE, JOIN, ORDER BY, pagination)?
  → YES: Integration test (real DB)
  → NO ↓

Does it cross module boundaries (two+ modules involved)?
  → YES: Integration test (multi-step)
  → NO ↓

Is it a critical business journey (blocks revenue or core workflow)?
  → YES: E2E test
  → NO ↓

Is it trivial CRUD (no branching, no side effects)?
  → YES: Skip. Existing integration tests are sufficient.
  → NO: Unit test if logic is complex enough.
```

---

### Step 3: Generate Matrix — Business Scenarios as Rows

Build an exhaustive test matrix. Rows are business scenarios. Columns are roles × outcomes × edge cases.

**Template:**

| Business Scenario | SALE | APPROVER | ADMIN | Unauthenticated |
|---|---|---|---|---|
| {scenario 1} | {outcome} | {outcome} | {outcome} | {outcome} |
| {scenario 2} | {outcome} | {outcome} | {outcome} | {outcome} |

**Example (Property Transitions):**

| Business Scenario | SALE | APPROVER | ADMIN | Unauthenticated |
|---|---|---|---|---|
| Agent submits draft for approval | → POST_PENDING + approval + notification | → AVAILABLE directly | → AVAILABLE directly | 401 |
| Agent submits other agent's draft | 403 | — | — | — |
| Agent withdraws pending request | → Reverts to previous status | 403 | 403 | 401 |
| Agent reports deposit | → DEPOSIT_PENDING + approval | → DEPOSITED directly | → DEPOSITED directly | 401 |
| Deposit with past contract date | 403 | 403 | 403 | 401 |
| Agent cancels deposit | → CANCEL_PENDING + approval | → AVAILABLE directly | → AVAILABLE directly | 401 |
| Agent completes sale | → COMPLETE_PENDING + approval | → COMPLETED directly | → COMPLETED directly | 401 |
| Admin approves pending request | — | Applies changes + status update | Applies changes + status update | 401 |
| Admin rejects pending request | — | Reverts to previous status | Reverts to previous status | 401 |
| Double approval prevention | — | 409 | 409 | — |

**For each cell, define:**
- What status change occurs
- Whether an approval is created
- Whether a notification is sent
- What error code is returned (if applicable)

---

### Step 4: Write — Tests That Read Like User Stories

#### Unit Tests

**File organization:** One file per facade function, named by business scenario.

```
tests/test_{module}/
  test_agent_creates_property_draft.py
  test_agent_submits_draft_for_approval.py
  test_admin_approves_pending_request.py
  test_customer_makes_deposit.py
  ...
```

**Function naming:** Each function is a complete business sentence.

**Template:**

```python
import pytest
from unittest.mock import AsyncMock
from src.modules.{module}.facades.{facade} import {facade_function}


async def test_{actor}_{action}_{expected_outcome}():
    """{Human-readable description of the business scenario.}"""
    # Arrange
    mock_repo = AsyncMock(spec=XxxRepo)
    mock_repo.get.return_value = build_entity(status="{starting_status}", ...)
    mock_other_repo = AsyncMock(spec=OtherRepo)

    # Act
    result = await {facade_function}(
        entity_id=...,
        body=...,
        current_user={actor_user},
        repo=mock_repo,
        other_repo=mock_other_repo,
    )

    # Assert — business outcomes
    assert result.status == "{expected_status}"
    assert result.{field} == {expected_value}
    mock_repo.save.assert_called_once()
    mock_other_repo.{method}.assert_called_once()


async def test_{actor}_{action}_{error_condition}_fails():
    """{Description of what goes wrong and why.}"""
    # Arrange
    mock_repo = AsyncMock(spec=XxxRepo)
    mock_repo.get.return_value = build_entity(status="{wrong_status}", ...)

    # Act + Assert
    with pytest.raises(ForbiddenError, match="{business error message}"):
        await {facade_function}(
            entity_id=...,
            body=...,
            current_user={actor_user},
            repo=mock_repo,
        )
```

**What to assert (business outcomes):**
- Status changed to expected value
- Approval created / not created
- Notification sent / not sent
- Error raised with business message (not HTTP code)
- Field values updated correctly
- Relationships maintained

**What NOT to assert in unit tests:**
- HTTP status codes (that's integration/E2E)
- Database queries (that's integration)
- JSON response format (that's integration)

#### Exhaustive Matrix for Unit Tests

For each facade, generate tests covering:

| Dimension | Values to Test |
|---|---|
| **Roles** | Every role that can call this facade (SALE, APPROVER, ADMIN) |
| **Starting statuses** | Every status the facade accepts (draft, available, deposited, ...) |
| **Error codes** | 401 (unauthenticated), 403 (forbidden), 404 (not found), 409 (conflict) |
| **Edge cases** | Empty input, null fields, boundary values, already-processed |
| **Side effects** | Notification sent/not sent, approval created/not created |
| **Ownership** | Owner vs non-owner (for SALE role restrictions) |

**Example matrix for `submit_property`:**

| Role | Starting Status | Expected Outcome |
|---|---|---|
| SALE (owner) | DRAFT | → POST_PENDING, approval created, notification sent |
| SALE (non-owner) | DRAFT | 403 |
| APPROVER | DRAFT | → AVAILABLE, no approval, no notification |
| ADMIN | DRAFT | → AVAILABLE, no approval, no notification |
| Any | POST_PENDING | 403 (wrong status) |
| Any | AVAILABLE | 403 (wrong status) |
| Unauthenticated | DRAFT | 401 |

#### Integration Tests

**When to use:** SQL queries, auth middleware, cross-module workflows, multi-step orchestration.

**File organization:** One file per business flow or query operation.

```
tests/test_property_flow/
  test_agent_posts_property_admin_approves.py
  test_deposit_flow_with_notification.py
  ...
```

**Function naming:** Describes the full business flow.

**Template:**

```python
async def test_{flow_name}(client, db_session, auth_headers, ...):
    """{Description of the complete business flow being tested.}"""
    # Step 1: {Business action}
    resp1 = await client.post("/endpoint", json={...}, headers=auth_headers)
    assert resp1.status_code == 201
    entity_id = resp1.json()["id"]

    # Step 2: {Business action}
    resp2 = await client.post(f"/endpoint/{entity_id}/action", headers=auth_headers)
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "{expected_status}"

    # Verify side effects in DB
    result = await db_session.execute(
        select(Entity).where(Entity.id == entity_id)
    )
    entity = result.scalars().first()
    assert entity.status == "{expected_status}"
```

**What to test in integration:**

| Category | What | 1 Test Per |
|---|---|---|
| **SQL queries** | Filter, sort, pagination, search | Each filter/sort/pagination operation |
| **Auth middleware** | `Depends(require_auth)`, `Depends(require_role)` | Each endpoint group (not each endpoint) |
| **Cross-module** | Notification created when property status changes | Each cross-module event |
| **Multi-step** | Create → Submit → Approve → Available | Each critical workflow |
| **Transactions** | Rollback on error, commit on success | Each transaction boundary |

#### E2E Tests

**When to use:** Critical business journeys only. ≤10 tests total.

**File organization:** One file per critical journey.

```
tests/test_e2e/
  test_complete_property_lifecycle.py
  test_deposit_and_sale_flow.py
  ...
```

**Function naming:** Describes the complete user journey.

**Template:**

```python
async def test_{journey_name}(client, db_session, ...):
    """End-to-end: {Complete business journey description}."""
    # This test exercises the full HTTP stack against a real database.
    # It verifies the entire business flow works end-to-end.

    # Step 1: {First business action}
    # Step 2: {Second business action}
    # ...
    # Final: Verify the business outcome
```

**What qualifies as E2E:**
- Core revenue workflow (create → list → deposit → complete)
- Critical security flow (login → auth → role check)
- Data integrity flow (create → update → verify persistence)

**What does NOT qualify:**
- Individual CRUD operations (integration is enough)
- Error handling (unit + integration covers it)
- Search/filter (integration covers it)

---

### Step 5: Verify — PO-Readable

After writing all tests:

1. **Run pytest** — confirm all tests pass
2. **Read every test name aloud** — would a product owner understand it?
3. **Check coverage:**
   - Every facade function has unit tests covering all roles × statuses
   - Every status transition has at least one test
   - Every error code (401, 403, 404, 409, 422) has at least one test
4. **Check no duplication:**
   - No integration test duplicates what a unit test already covers
   - No E2E test duplicates what an integration test already covers
5. **Check E2E count:** ≤ 10 tests total

---

## Test Naming — Complete Reference

### Pattern

```
test_{actor}_{action}_{expected_outcome}
```

### Actors

| Actor | When to Use |
|---|---|
| `agent` | SALE role performing an action |
| `admin` | ADMIN role performing an action |
| `approver` | APPROVER role performing an action |
| `customer` | External user (deposit, complete) |
| `system` | Automated behavior (expiration, cleanup) |
| `unauthenticated_user` | No auth token |
| `user` | Generic authenticated user (any role) |

### Actions

Use business verbs, not HTTP methods:

| ❌ HTTP | ✅ Business |
|---|---|
| `creates` (POST) | `creates`, `submits`, `publishes`, `registers` |
| `updates` (PUT) | `edits`, `modifies`, `changes`, `updates` |
| `deletes` (DELETE) | `removes`, `deactivates`, `cancels` |
| `approves` (POST) | `confirms`, `approves`, `authorizes` |
| `rejects` (POST) | `rejects`, `denies`, `refuses` |
| `gets` (GET) | `views`, `retrieves`, `browses` |
| `lists` (GET) | `browses`, `views`, `searches` |

### Outcomes

Describe the business result:

| ❌ Technical | ✅ Business |
|---|---|
| `returns_200` | `receives_property_list` |
| `returns_403` | `is_rejected_with_forbidden` |
| `returns_404` | `property_is_not_found` |
| `returns_409` | `conflict_is_prevented` |
| `status_changes_to_available` | `property_becomes_available` |
| `notification_is_sent` | `receives_notification` |
| `approval_is_created` | `approval_request_is_created` |

### 15 Complete Examples

```
test_agent_creates_property_draft
test_agent_publishes_property_for_approval
test_admin_approves_pending_listing_request
test_approver_rejects_property_edit
test_customer_makes_deposit_on_property
test_agent_reports_property_as_sold
test_system_expires_overdue_deposit_automatically
test_sale_cannot_edit_other_agents_property
test_unauthenticated_user_cannot_create_property
test_wrong_password_returns_generic_error
test_agent_withdraws_pending_request
test_system_prevents_double_approval
test_buyer_finds_properties_within_budget
test_agent_receives_real_time_approval_notification
test_admin_removes_unlisted_property
```

---

## Unit Test Patterns

### Mock Setup

```python
from unittest.mock import AsyncMock, MagicMock

# Mock the repository
mock_repo = AsyncMock(spec=XxxRepo)
mock_repo.get.return_value = build_entity(...)
mock_repo.save.return_value = None

# Mock multiple repos
mock_property_repo = AsyncMock(spec=PropertyRepo)
mock_approval_repo = AsyncMock(spec=ApprovalRepo)
mock_notification_service = AsyncMock(spec=NotificationService)
```

### Dependency Override (for integration-style unit tests)

```python
from src.platform.dependencies import get_db

async def test_something(client, db_session):
    # Override with real DB session
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        response = await client.get("/endpoint")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.pop(get_db, None)
```

### Builder Functions

Create reusable builders for domain entities:

```python
def build_property(
    status="draft",
    created_by=AGENT_UUID,
    transaction_type="sell",
    property_type="HOUSE",
    **overrides
):
    return PropertyEntity(
        id=uuid4(),
        status=status,
        created_by_id=created_by,
        transaction_type_id=transaction_type,
        property_type_id=property_type,
        **overrides
    )
```

### Asserting Side Effects

```python
# Notification sent
mock_notification_service.notify_admins_and_approvers.assert_called_once()
call_args = mock_notification_service.notify_admins_and_approvers.call_args
assert call_args.kwargs["event_type"] == NotificationType.LISTING_POST_CREATED

# Approval created
mock_approval_repo.create.assert_called_once()
created_approval = mock_approval_repo.create.call_args[0][0]
assert created_approval.status == ApprovalStatus.PENDING

# Notification NOT sent (admin direct action)
mock_notification_service.notify_admins_and_approvers.assert_not_called()
```

---

## Integration Test Patterns

### Real DB Setup

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def client(db_session):
    """HTTP client with real DB session."""
    from src.main import app
    from src.platform.dependencies import get_db

    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)
```

### Auth Headers

```python
@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
def agent_headers(agent_token):
    return {"Authorization": f"Bearer {agent_token}"}
```

### DB Verification

```python
from sqlalchemy import select
from src.data.entities.notification import NotificationEntity

async def test_notification_created(client, db_session, agent_headers):
    # Act
    response = await client.post("/properties", json=payload, headers=agent_headers)

    # Verify in DB
    result = await db_session.execute(
        select(NotificationEntity).where(
            NotificationEntity.user_id == APPROVER_UUID
        )
    )
    notifications = result.scalars().all()
    assert len(notifications) == 1
    assert notifications[0].event_type == "listing_post_created"
    assert notifications[0].is_read is False
```

### Multi-Step Flow

```python
async def test_submit_approve_flow(client, db_session, agent_headers, admin_headers):
    """Agent submits draft, admin approves, property becomes available."""
    # Create
    create_resp = await client.post("/properties", json=property_payload, headers=agent_headers)
    prop_id = create_resp.json()["id"]

    # Submit
    submit_resp = await client.post(
        f"/properties/{prop_id}/transitions/submit",
        json={"notes": None},
        headers=agent_headers,
    )
    assert submit_resp.json()["status"] == "post_pending"

    # Get approval ID
    approvals_resp = await client.get("/approvals", headers=admin_headers)
    approval_id = approvals_resp.json()["data"][0]["id"]

    # Approve
    approve_resp = await client.post(
        f"/approvals/{approval_id}/approve",
        json={"reason": None},
        headers=admin_headers,
    )
    assert approve_resp.status_code == 204

    # Verify final state
    get_resp = await client.get(f"/properties/{prop_id}", headers=agent_headers)
    assert get_resp.json()["status"] == "available"
```

---

## Anti-Patterns

| ❌ Anti-Pattern | Why It's Wrong | ✅ Fix |
|---|---|---|
| `test_create_property_201` | Technical, describes HTTP not business | `test_agent_creates_property_draft` |
| `test_approve_sets_status_to_available` | Describes code behavior | `test_approver_confirms_property_listing` |
| `test_put_endpoint` | Describes HTTP method | `test_agent_edits_listed_property` |
| Unit test for simple CRUD Tag creation | No business logic to test | Keep existing integration test |
| E2E test for login flow | Not critical enough for E2E | Integration test is sufficient |
| Integration test testing what unit already covers | Duplication | Remove integration test |
| Test that requires reading code to understand name | Not PO-readable | Rewrite in business language |
| Mocking everything in integration test | Defeats purpose of integration | Use real DB for integration |
| Testing HTTP status codes only | Misses business outcomes | Assert business state changes |
| 50+ E2E tests | Too many, slow, brittle | Keep ≤10, cover only critical journeys |

---

## Verification Checklist

Before submitting, verify:

- [ ] Every test name is in business language (PO-readable)
- [ ] Every facade function has unit tests covering all roles × statuses
- [ ] Every status transition has at least one test
- [ ] Every error code (401, 403, 404, 409, 422) has at least one test
- [ ] No integration test duplicates a unit test
- [ ] No E2E test duplicates an integration test
- [ ] E2E tests are ≤ 10 total
- [ ] All tests pass (`pytest`)
- [ ] Test names follow `test_{actor}_{action}_{outcome}` pattern
- [ ] Unit tests mock repos, not HTTP layer
- [ ] Integration tests use real DB for SQL operations
- [ ] Multi-step flows are tested as complete journeys

---

**Remember:** A test name that a product owner can't understand is a test that doesn't communicate its value. Write tests that tell the story of what the system does for the business.
