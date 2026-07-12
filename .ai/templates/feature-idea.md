# Feature Idea: [Feature Name]

> **Date:** [YYYY-MM-DD]
> **Author:** [Name]
> **Status:** Idea / In Progress / Done

---

## Your Idea

**What do you want to build?**

[Describe your idea in 1-2 sentences]

---

## Questions & Answers

### 1. What is the feature in one sentence?

[Answer]

### 2. Who is the user?

[Answer]

### 3. What problem does it solve?

[Answer]

### 4. How should it work?

[Answer]

### 5. What are the constraints?

[Answer]

### 6. How do we know it's done?

[Answer]

### 7. What are the edge cases?

[Answer]

### 8. What existing code can we reuse?

[Answer]

---

## Generated Requirement (for AI Agent)

### Summary

[One sentence describing what this feature does]

### User Story

**As a** [user role]
**I want to** [action/goal]
**So that** [benefit/value]

### Acceptance Criteria

Write acceptance criteria as test-like scenarios (business-language names).

- [ ] test_[actor]_[action]_[expected_outcome]
- [ ] test_[actor]_[action]_[expected_outcome]
- [ ] test_[actor]_[action]_[expected_outcome]

**Example format:**
```
- [ ] test_agent_receives_notification_on_property_approval
- [ ] test_notification_contains_property_details
- [ ] test_unauthenticated_user_receives_no_notification
```

### Constraints

- [Constraint 1: performance, security, etc.]
- [Constraint 2]
- [Constraint 3]

### Edge Cases

Write edge cases as test-like scenarios.

- [ ] test_[actor]_[error_condition]_[expected_behavior]
- [ ] test_[actor]_[error_condition]_[expected_behavior]

**Example format:**
```
- [ ] test_notification_not_sent_on_approval_failure
- [ ] test_notification_sent_even_if_user_is_offline
```

### Existing Code to Reuse

| Component | Location | How to Reuse |
|-----------|----------|--------------|
| [Entity/Repo/Facade] | [File path] | [What to extend] |
| [UI Component] | [File path] | [What to extend] |

### Dependencies

- [ ] [Dependency 1]
- [ ] [Dependency 2]

### Tests Required

| Type | Scope |
|------|-------|
| Unit | [What to test] |
| Integration | [What to test] |
| E2E | [What to test] |

---

## How to Use This Document

### For AI Coding Agent

Copy the **Generated Requirement** section above and give it to your AI coding agent. The agent will:

1. Read the acceptance criteria (test-like scenarios)
2. Read the edge cases (test-like scenarios)
3. Read the existing code to reuse
4. Implement the feature following `backend-dev` / `frontend-dev` patterns
5. Generate tests following `backend-test` patterns

### For `workflow` Skill

Copy the **Generated Requirement** section above and use it as input for the `workflow` skill:

```
User: [Paste the Generated Requirement section]
Agent: [Uses workflow skill to plan and implement]
```

### For Manual Development

Use the acceptance criteria and edge cases as your implementation checklist:

1. Implement each acceptance criteria
2. Handle each edge case
3. Write tests for each scenario
4. Verify all checkboxes are checked
