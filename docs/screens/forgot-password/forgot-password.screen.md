# Forgot Password / Reset Password Screen

## APIs

### Step 1 — Forgot Password
`POST /api/v1/auth/forgot-password`

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `email` | string | yes | 1-255 chars |

**Response (200)**
```json
{
  "message": "string"
}
```

### Step 2 — Reset Password
`POST /api/v1/auth/reset-password`

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `token` | string | yes | min 1 char (obtained from email link) |
| `new_password` | string | yes | min 6 chars |

**Response (200)**
```json
{
  "message": "string"
}
```

### Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

## Step 1 — Forgot Password Screen

### Idle
- Single field: email input with email keyboard type
- Submit button ("Send Reset Link")
- Link back to login screen ("Back to Sign In")

### Loading
- Submit button shows spinner, field disabled
- "Sending..." text on button

### Success
- Show confirmation message from API response
- "Check your email for the password reset link" with email icon
- Link back to login screen

### Error — Validation (422)
- Highlight email field with red border
- Show error below field: "Please enter a valid email address"

### Error — Network / Server Error
- Banner: "Unable to send reset link. Please try again."
- Field remains editable

---

## Step 2 — Reset Password Screen

### Idle
- Two fields: new password (masked, with show/hide toggle), confirm password (masked)
- Optional: password strength indicator (weak/medium/strong based on 6+ char minimum)
- Submit button ("Reset Password")
- Token is embedded in URL or passed from step 1

### Loading
- Submit button shows spinner, fields disabled
- "Resetting password..." text on button

### Success
- "Password reset successfully" with checkmark icon
- "Sign in with your new password" link → redirect to login screen

### Error — Validation (422)
- Invalid/expired token: banner "This reset link has expired. Please request a new one."
- Weak password: inline error below new password field "Password must be at least 6 characters"
- Passwords don't match: client-side validation before API call

### Error — Network / Server Error
- Banner: "Unable to reset password. Please try again."
- Fields remain editable
