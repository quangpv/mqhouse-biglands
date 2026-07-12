# Bug Investigation: [Bug Title]

> **Date:** [YYYY-MM-DD]
> **Author:** [Name]
> **Status:** Open / Investigating / Fixed / Won't Fix
> **Priority:** Critical / High / Medium / Low

---

## Expected Behavior

**What should happen?**

[Describe the correct behavior in 1-2 sentences]

**Where is this documented?**

- [ ] API contract (`docs/contract/`)
- [ ] Architecture docs (`docs/architecture/`)
- [ ] Existing test
- [ ] User expectation

---

## Actual Behavior

**What actually happened?**

[Describe the incorrect behavior in 1-2 sentences]

**Error message (if any):**

```
[Paste error message or stack trace]
```

---

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Observe bug]

**Reproduction rate:** Always / Sometimes / Rare

---

## Timeline

**When did this start happening?**

- [ ] After deploying [version/date]
- [ ] After changing [specific code]
- [ ] After [external event]
- [ ] Unknown

**When was it first reported?**

[Date and time]

---

## Recent Changes

| Date | Change | Author | Related? |
|------|--------|--------|----------|
| [Date] | [What changed] | [Who] | Yes / No / Maybe |

**Files changed recently:**

- [ ] `backend/src/modules/[module]/[file].py`
- [ ] `frontend/src/pages/[feature]/[file].tsx`
- [ ] `docs/contract/[file].md`

---

## Consistency Pattern

**Is this consistent or intermittent?**

- [ ] Happens every time
- [ ] Happens with specific conditions
- [ ] Happens randomly
- [ ] Happens under load

**Conditions (if specific):**

- [ ] User role: [SALE / APPROVER / ADMIN]
- [ ] Property status: [draft / available / deposited]
- [ ] Time of day: [Morning / Afternoon / Night]
- [ ] Browser: [Chrome / Safari / Firefox]
- [ ] Device: [Desktop / Mobile]

---

## Affected Scope

**Users affected:**

- [ ] All users
- [ ] Specific role: [Role name]
- [ ] Specific user: [User ID/name]
- [ ] Specific organization: [Org name]

**Systems affected:**

- [ ] Backend API
- [ ] Frontend UI
- [ ] Database
- [ ] WebSocket
- [ ] Notifications
- [ ] File storage

---

## Impact

**How severe is this?**

| Impact | Details |
|--------|---------|
| Business | [Revenue, workflow, compliance impact] |
| Users | [Number of users affected, workarounds available] |
| Data | [Data integrity, loss, corruption risk] |
| Timeline | [Urgency, deadline impact] |

---

## Investigation Notes

**What I've checked so far:**

- [ ] Checked logs: [Findings]
- [ ] Checked database: [Findings]
- [ ] Checked recent deployments: [Findings]
- [ ] Checked error tracking: [Findings]

**Hypotheses:**

1. [Hypothesis 1] — [Evidence for/against]
2. [Hypothesis 2] — [Evidence for/against]

---

## Root Cause

**What caused this bug?**

[Describe the root cause once identified]

**Code location:**

- File: [path/to/file.py]
- Function: [function_name]
- Line: [line_number]

---

## Fix

**How was this fixed?**

[Describe the fix]

**Files changed:**

- [ ] `backend/src/modules/[module]/[file].py`
- [ ] `frontend/src/pages/[feature]/[file].tsx`
- [ ] `tests/test_[module]/test_[file].py`

---

## Verification

**How do we verify the fix?**

- [ ] Reproduction steps no longer trigger bug
- [ ] Existing tests still pass
- [ ] New test added for this bug
- [ ] Manual testing completed

**Test added:**

```python
def test_[actor]_[action]_[expected_outcome]():
    """[Business-language description of the bug fix]"""
    # Test code here
```

---

## Prevention

**How do we prevent this in the future?**

- [ ] Added test coverage for this scenario
- [ ] Updated documentation
- [ ] Added validation/check
- [ ] Improved error handling
