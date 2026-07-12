# Instruction for Programmer

> **Never write code before asking the right questions.**

The difference between a junior and senior developer is the questions they ask BEFORE writing code.

---

## Scenario 1: Starting a New Project

**Core question:** "What problem are we solving?"

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What problem are we solving? | Defines scope and purpose |
| 2 | Who is the user? | Shapes UI/UX decisions |
| 3 | What are the constraints? | Sets boundaries (time, tech, budget) |
| 4 | What does success look like? | Defines completion criteria |
| 5 | What are the risks? | Identifies blockers early |
| 6 | What existing solutions exist? | Avoids reinventing the wheel |
| 7 | What scale do we need? | Shapes architecture decisions |
| 8 | What security requirements? | Defines protection level |

**Checklist:**
- [ ] Problem statement written
- [ ] User roles identified
- [ ] Constraints documented
- [ ] Success criteria defined
- [ ] Risks listed
- [ ] Existing solutions reviewed
- [ ] Scale requirements clarified
- [ ] Security requirements defined

**Next step:** Use `workflow` skill → Step 1: Clarify

---

## Scenario 2: Adding a New Feature

**Core question:** "What does the user need?"

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What problem does this feature solve? | Justifies the effort |
| 2 | Who is the user? | Shapes implementation |
| 3 | What are the acceptance criteria? | Defines "done" |
| 4 | What are the edge cases? | Prevents bugs |
| 5 | What existing code can we reuse? | Saves time |
| 6 | What are the dependencies? | Identifies blockers |
| 7 | How does this affect existing features? | Prevents regressions |
| 8 | What tests do we need? | Ensures quality |

**Checklist:**
- [ ] Problem statement written
- [ ] User roles identified
- [ ] Acceptance criteria defined (Given/When/Then)
- [ ] Edge cases listed
- [ ] Existing code reviewed for reuse
- [ ] Dependencies identified
- [ ] Impact on existing features assessed
- [ ] Test strategy defined

**Next step:** Use `workflow` skill → Step 1: Clarify

---

## Scenario 3: Investigating a Bug

**Core question:** "What actually happened?"

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What is the expected behavior? | Defines "correct" |
| 2 | What is the actual behavior? | Defines the problem |
| 3 | What are the steps to reproduce? | Enables debugging |
| 4 | When did this start happening? | Identifies trigger |
| 5 | What changed recently? | Finds root cause |
| 6 | Is this consistent or intermittent? | Shapes investigation |
| 7 | What are the affected users/systems? | Defines scope |
| 8 | What is the impact? | Prioritizes fix |

**Checklist:**
- [ ] Expected behavior documented
- [ ] Actual behavior documented
- [ ] Reproduction steps provided
- [ ] Timeline established
- [ ] Recent changes identified
- [ ] Consistency pattern determined
- [ ] Affected scope defined
- [ ] Impact assessed

**Next step:** Read `docs/architecture/backend.md` → State machine and error handling

---

## Scenario 4: Feature Idea → Requirement

**Core question:** "What do you want to build?"

Turn a vague idea into a structured requirement that an AI coding agent can implement.

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What is the feature in one sentence? | Defines scope |
| 2 | Who is the user? | Shapes implementation |
| 3 | What problem does it solve? | Justifies effort |
| 4 | How should it work? | Describes behavior |
| 5 | What are the constraints? | Sets boundaries |
| 6 | How do we know it's done? | Defines completion |
| 7 | What are the edge cases? | Prevents bugs |
| 8 | What existing code can we reuse? | Saves time |

**Checklist:**
- [ ] Feature summary written
- [ ] User role identified
- [ ] Problem statement written
- [ ] Behavior described
- [ ] Constraints listed
- [ ] Acceptance criteria defined (test-like scenarios)
- [ ] Edge cases listed (test-like scenarios)
- [ ] Existing code reviewed

**Output:** Use `feature-idea.md` template → Get requirement document → Give to AI agent

**Next step:** Give the generated requirement to `workflow` skill or AI coding agent

---

## Question Quality Framework

### Good Questions (Use These)

| Characteristic | Example |
|----------------|---------|
| Specific | "What happens when an agent tries to approve their own property?" |
| Actionable | "Should we use WebSocket or polling for notifications?" |
| Focused | "What is the timeout for file uploads?" |
| Testable | "Does the deposit flow work with past contract dates?" |

### Bad Questions (Avoid These)

| Characteristic | Example |
|----------------|---------|
| Vague | "How does the property feature work?" |
| Unactionable | "What should we do about the bug?" |
| Unfocused | "What are the requirements?" |
| Untestable | "Is the system good?" |

---

## Quick Prompt Template

One-line format for asking AI agents to code:

### Feature
```
Add [feature] for [role] ([constraints])
```

### Bug
```
Fix [bug] where [symptom] ([scope])
```

### Improvement
```
Improve [feature] to [goal] ([constraint])
```

### Removal
```
Remove [feature] (replace with [alternative])
```

### Examples

| Type | One-Liner |
|------|-----------|
| Feature | `Add property notification for agents when approved (real-time, max 100/user)` |
| Bug | `Fix property creation bug where draft status not set (agent role, POST endpoint)` |
| Improvement | `Improve property search to support Vietnamese normalization (accent-insensitive)` |
| Removal | `Remove deprecated file upload endpoint (replace with new /files endpoint)` |

### Quick Reference

```
# Feature
Add [feature] for [role] ([constraints])

# Bug
Fix [bug] where [symptom] ([scope])

# Improvement
Improve [feature] to [goal] ([constraint])

# Removal
Remove [feature] (replace with [alternative])
```

---

## Clarification One-Liner

When you have a vague idea, ask AI agent to help clarify:

### Feature
```
I want to [vague idea]. Help me clarify: who is the user, what problem does it solve, what are the constraints, and how do we know it's done?
```

### Bug Fix
```
I found a bug: [vague description]. Help me clarify: what is the expected behavior, what is the actual behavior, what are the steps to reproduce, and what is the impact?
```

### Flow

```
Vague idea → Clarification one-liner → AI agent asks questions → Answers → Clear one-liner → Code
```

### Examples

| Type | Clarification One-Liner |
|------|------------------------|
| Feature | `I want to add notifications. Help me clarify: who is the user, what problem does it solve, what are the constraints, and how do we know it's done?` |
| Bug | `I found a bug where property status doesn't update. Help me clarify: what is the expected behavior, what is the actual behavior, what are the steps to reproduce, and what is the impact?` |

---

## Quick Reference Card

### Starting a New Project

```
1. What problem are we solving?
2. Who is the user?
3. What are the constraints?
4. What does success look like?
5. What are the risks?
6. What existing solutions exist?
7. What scale do we need?
8. What security requirements?
```

### Adding a New Feature

```
1. What problem does this feature solve?
2. Who is the user?
3. What are the acceptance criteria?
4. What are the edge cases?
5. What existing code can we reuse?
6. What are the dependencies?
7. How does this affect existing features?
8. What tests do we need?
```

### Investigating a Bug

```
1. What is the expected behavior?
2. What is the actual behavior?
3. What are the steps to reproduce?
4. When did this start happening?
5. What changed recently?
6. Is this consistent or intermittent?
7. What are the affected users/systems?
8. What is the impact?
```

### Feature Idea → Requirement

```
1. What is the feature in one sentence?
2. Who is the user?
3. What problem does it solve?
4. How should it work?
5. What are the constraints?
6. How do we know it's done?
7. What are the edge cases?
8. What existing code can we reuse?
```

---

## Integration with Skills

| Step | What to Use |
|------|-------------|
| 1. Think | This instruction — ask the right questions |
| 2. Plan | `workflow` skill — 5-step implementation process |
| 3. Build | `backend-dev` / `frontend-dev` — coding patterns |
| 4. Verify | `backend-test` — test generation |

---

## Templates

Use these templates to document your answers:

| Scenario | Template | Location |
|----------|----------|----------|
| New Project | `new-project.md` | `.ai/templates/` |
| New Feature | `new-feature.md` | `.ai/templates/` |
| Bug Investigation | `bug-investigation.md` | `.ai/templates/` |
| Feature Idea | `feature-idea.md` | `.ai/templates/` |
