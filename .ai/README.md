# Entry Point

> **Start here every session.**

---

## When to Read `instruction.md`

| Situation | Action |
|-----------|--------|
| Starting any new work | Read `instruction.md` first — ask the right questions before coding |
| Vague idea or request | Use **Scenario 4** (Feature Idea → Requirement) to clarify |
| New feature | Use **Scenario 2** checklist |
| Bug report | Use **Scenario 3** checklist |
| New project | Use **Scenario 1** checklist |

**Rule:** Never write code before finishing the relevant checklist in `instruction.md`.

---

## When to Use Which Skill

| I want to... | Use Skill | What It Does |
|--------------|-----------|--------------|
| Plan a feature from requirement | `workflow` | Clarify → Explore → Design → Plan → Execute |
| Build a backend endpoint / module | `backend-dev` | FastAPI patterns, Router→Facade→Repo |
| Build a frontend page / component | `frontend-dev` | View→Facade→Data architecture |
| Write tests for a feature | `backend-test` | Business-language test generation |
| Quick bug fix or refactor | None — read `instruction.md` Scenario 3, then implement directly | — |

### Decision Flowchart

```
Is this a new feature or feature change?
  → YES → Use `workflow` skill (full 5-step process)
  → NO ↓

Is this a bug?
  → YES → Read `instruction.md` Scenario 3 → Fix → Use `backend-test` if no coverage
  → NO ↓

Is this a refactor or improvement?
  → YES → Read existing code → Implement using `backend-dev` / `frontend-dev` patterns
  → NO → Just code it

Is this writing tests?
  → YES → Use `backend-test` skill
```

---

## Business Rules Management

Use this for any rule change: adding a new rule, strengthening an existing one, or resolving a conflict.

| Situation | Case |
|-----------|------|
| Rule doesn't exist in `docs/contract/` or isn't enforced in code | **New** |
| Rule exists but is too loose, has gaps, or isn't strictly enforced | **Strengthen** |
| New rule contradicts an existing rule | **Conflict** |

---

### Prompt

```
Business rule change: [describe the rule]

Case: [New / Strengthen / Conflict]

If Strengthen — Current rule: [quote from docs/contract/]
If Strengthen — Problem: [what is too loose]
If Conflict — Existing rule: [quote from docs/contract/]
If Conflict — Conflict type: [RBAC / State Machine / Cross-Domain]

Steps:
1. Identify — find the exact location in `docs/contract/` (or confirm it doesn't exist)
2. Decide — determine what changes:
   - New: add rule to the correct domain file
   - Strengthen: override the existing rule
   - Conflict: determine which rule wins, then override the loser
3. Update docs — write the final rule into `docs/contract/`
4. Update code — enforce the rule in the appropriate layer:
   - Backend: facade (business logic) or router (RBAC)
   - Frontend: facade action hook (validation) or mapper (data transformation)
5. Update tests — add or rename tests using `backend-test` patterns (business-language naming)
6. Check cross-domain — does this change affect other domains? Update `docs/contract/README.md` interaction map if needed
```

### Example

```
Business rule change: "Sales cannot edit AVAILABLE properties directly — must go through approval"

Case: Strengthen

Current rule: docs/contract/properties.md — "Sales staff can only update their own properties"
Problem: No status restriction — Sales can edit AVAILABLE listings directly

Steps:
1. Location: docs/contract/properties.md line 145
2. Decide: override — Sales edits on AVAILABLE must route through EDIT_PENDING
3. Update docs: "Sales can edit DRAFT/POST_PENDING directly. AVAILABLE requires EDIT_PENDING approval."
4. Update code: PUT /properties/{id} facade — add status check for Sales role
5. Update tests: test_sale_cannot_edit_available_property_directly
6. Cross-domain: EDIT_PENDING flow already documented — no change needed
```

### Business Rule Checklist

When adding, strengthening, or changing business rules, check:

- [ ] **RBAC** — Who can do this? (SALE, APPROVER, ADMIN)
- [ ] **Status transitions** — What states allow this action? What state results?
- [ ] **Validation** — Required fields, formats, ranges, constraints
- [ ] **Ownership** — Can the user act on resources they don't own?
- [ ] **Side effects** — Notifications, approvals, WebSocket events?
- [ ] **Edge cases** — Double submit, race conditions, expired data?
- [ ] **Documentation** — Is the rule in `docs/contract/`?
- [ ] **Tests** — Is there a test with business-language name?
- [ ] **Cross-domain** — Does this change affect other domains?
