---
name: api-contract-docs
description: Generate or audit API contract documentation for any project. Use when the user asks to "document the API", "write/generate contract docs", "create API documentation", "analyze/audit existing API docs", or wants a domain-organized contract doc set (README + types + per-domain files) from requirements, PRDs, Swagger/OpenAPI, Postman collections, or backend code.
---

# API Contract Documentation

Generate a maintainable, domain-organized API contract documentation set for a project, or audit an existing set for completeness and consistency. The pattern is derived from a production contract doc folder (`README.md` index + `types.md` schemas + one markdown file per domain + a system file for non-CRUD features).

## When to Use

- A new project needs its API documented before or during development.
- Source material exists (requirements, PRD, legacy docs, Swagger/OpenAPI, Postman, backend code) and needs to become structured contract docs.
- An existing contract doc set needs a completeness/consistency audit.

## Input Sources

Gather from any combination of:

| Source | What to extract |
|---|---|
| Requirements / PRD | Business rules, roles, workflows, constraints |
| Swagger / OpenAPI | Endpoints, methods, schemas, params, responses |
| Postman collection | Endpoint inventory, request/response examples |
| Backend code (routes, controllers, entities) | Actual endpoint paths, access guards, DTOs, enums, statuses |
| Database schema | Entities, relationships, fields, constraints |
| Existing docs | Anything reusable, plus gaps to fill |

## Output File Layout

```
contract/
  README.md          # index + global rules + RBAC matrix + state machine + cross-domain map
  types.md           # all enums, base types, entities, request types, response types
  <domain>.md        # one file per domain (e.g. properties.md, auth.md, users.md)
  system.md          # non-CRUD / system / background features (WebSocket, cron jobs, public endpoints)
```

Conventions:
- Fixed names: `README.md` and `types.md`.
- Domain files: `kebab-case.md`, named with a plural domain noun (`users.md`, `properties.md`, `notifications.md`).
- Small APIs may collapse to a single README; large APIs split by domain. Never put endpoint details in `types.md` or schema details in domain files.

## Generation Workflow

1. **Inventory source material.** List every endpoint (method + path), entity, enum, role, and status you can find. Flag gaps where source material is missing or contradictory.
2. **Identify domains.** Group endpoints by resource/concern. Each resource gets its own file. Put cross-resource or global stuff in `README.md`; put non-HTTP features (scheduled jobs, WebSocket, realtime) in `system.md`.
3. **Extract global rules.** Authentication (session lifetimes, refresh, logout semantics), authorization (roles, permission rules), error response mapping, pagination defaults, privacy rules, and cross-cutting behaviors (auto-rejection cascades, notification fan-out, soft deletion).
4. **Build the RBAC matrix.** Endpoint × role (plus a `Public` column). Mark overrides with footnotes (e.g. `Y*` = owner-only) and explain the footnotes under the table.
5. **Build state machines.** For any statusful resource, draw the status flow as an ASCII diagram. Enumerate pending (approval-required) and terminal statuses. Document scheduled transitions (e.g. midnight expiry cron) separately.
6. **Write `types.md`.** Order: enums → base types → core entities → request types (grouped by domain) → response types (grouped by domain). Reference these by name from domain files.
7. **Write per-domain files.** One `## Global Rules` section, then one `##` section per endpoint, then `## Related` links.
8. **Write `system.md`.** Non-HTTP and system-scope features: public data (geography, master data), background jobs, WebSocket connections and events, admin backfills.
9. **Write `README.md`.** Global rules, RBAC matrix, state machine diagram(s), a cross-domain interaction map (ASCII), and a Domain Files index table.
10. **Run the QA checklist** below.

## Canonical Templates

### Domain file header

```markdown
# Properties

Prefix: `/properties`

See [types.md](./types.md) for request/response schemas. See [README.md](./README.md) for RBAC matrix and state machine diagram.

---
```

### Endpoint block

```markdown
## POST /properties

Desc: Create a property listing.

**Access:** Requires sign-in

**Rules:**
- Saving as draft saves privately; no approval needed; no one is notified.
- Publishing by Sales staff goes to the approval queue; admins and approvers are notified.
- Type guard applies for Sales staff and Approvers (see Global Rules).

**Request:** `CreatePropertyRequest`
**Response:** `PropertyResponse`
```

- `Desc:` is one sentence stating the action.
- `**Access:**` uses only the standard labels below.
- `**Rules:**` one deterministic complete sentence per bullet. Every branch must be stated (who / when / what happens).
- Use Markdown tables inside `Rules` for mappings (status → result, role → behavior, notification → recipient).
- `**Request:**`/`**Response:**` reference type names from `types.md`. Add inline status codes when not 200, e.g. `**Response:** `UserResponse` (201)`.

### Access labels

| Label | Meaning |
|---|---|
| `Public` | No sign-in required |
| `Requires sign-in` | Any authenticated user |
| `Admin only` | Only Admin role |
| `Admin or Approver` | Only those two roles |
| `Sales staff only` | Only the Sales role |
| `Owner only` | Only the resource creator (add role qualifiers if needed) |

### Type block (`types.md`)

```markdown
### Property
{
  id: UUID
  code: string                      // 14-char: YYMMDD + 7-digit random
  title: string | null
  status: Status
  price_per_m2: number | null       // computed: price / total_area
}
```

- Fenced code blocks; one field per line; `| null` marks optional; `//` comment notes format, defaults, computed values, or constraints.
- Enums are an inline list per value, e.g. `Status = [draft, available, soldout, ...]`.

### Global rules (`README.md`)

```markdown
## Global Rules

### Authentication
- Every action requires a signed-in session unless the endpoint is marked **Public**.
- Sessions last 24 hours; refresh sessions last 7 days.
- Signing out cancels the current session and all other active sessions.

### Error Responses
| Situation | What Happens |
|---|---|
| Resource not found | 404 — The requested item does not exist |
| Not signed in | 401 — Authentication required |
```

### RBAC matrix (`README.md`)

```markdown
## RBAC Matrix

| Endpoint | ADMIN | APPROVER | SALE | Public |
|---|---|---|---|---|
| `POST /auth/login` | - | - | - | Y |
| `PUT /properties/{id}` | Y* | Y* | Owner only | - |
```

### State machine (`README.md`)

```markdown
## Property State Machine

DRAFT ──────────────> POST_PENDING ──(approve)──> AVAILABLE
   │                       │         (reject)
   └───────────────────────┴──────> DRAFT
```

### Cross-domain interaction map (`README.md`)

```markdown
Properties ──triggers──> Approvals ──decides──> Properties (status change)
     │                      └──sends──> Notifications ──WebSocket──> Client
     └──records──> Status History
```

## Audit Workflow

When auditing existing contract docs, check:

1. **Required files exist**: `README.md`, `types.md`, and every expected domain file.
2. **Endpoint coverage**: every documented endpoint has `Desc`, `**Access:**`, `**Rules:**`, and `**Request:**`/`**Response:**` (or explicit `204 No Content`).
3. **RBAC matrix matches**: every endpoint in the matrix appears in a domain file and vice versa; role cells match the `**Access:**` labels.
4. **State machine is sound**: every status reachable, no unreachable transitions, terminal statuses identified, pending (approval-required) statuses enumerated.
5. **Schema references resolve**: every `Request`/`Response` reference exists in `types.md`; every enum used exists in the Enums section.
6. **Rules are deterministic**: no "maybe", "should", or ambiguous branches; each permission/branch states exactly who can do what.
7. **Cross-references resolve**: `## Related` links and `See [...]` links point to real files/sections.
8. **Global rules cover the obvious**: authn, authz, error responses, pagination, privacy. If a domain file repeats a rule that is truly global, it should move to `README.md`.
9. **System/background features documented**: scheduled jobs, WebSocket, and public endpoints live in `system.md`, not orphaned inside domain files.

## QA Checklist

- [ ] Every endpoint documented with method + full path.
- [ ] Every endpoint has `Desc`, `**Access:**`, `**Rules:**`, `**Request:**` (if body/params), `**Response:**`.
- [ ] RBAC matrix complete and consistent with endpoint files.
- [ ] Access labels use only the standard set.
- [ ] All roles, enums, statuses, and entities defined in `types.md`.
- [ ] State machine covers all statuses; pending and terminal statuses called out.
- [ ] Non-HTTP features in `system.md`.
- [ ] Global rules centralized in `README.md`, not duplicated per domain.
- [ ] All file links and type references resolve.
- [ ] Rules written as deterministic complete sentences; no ambiguity.
- [ ] Pagination, error mapping, and auth defaults stated in `README.md`.

## Adaptation Notes

- **Per project, regenerate**: domain list, RBAC matrix, state machines, entities, endpoints, and project-specific rules.
- **Reuse as-is**: the file layout, section templates, access labels, and QA checklist.
- **Scale to size**: a 5-endpoint API can live in one README; a large API (10+ resources, status workflows, roles) should follow the full split. Never force a tiny API into 10 near-empty files.
- **Language**: write docs in the project's language, but keep the structure and labels identical so rules stay machine-checkable.
- **Sources of truth**: when source material conflicts, prefer backend code and schema over prose requirements, and record the conflict in the doc rather than silently picking one.
