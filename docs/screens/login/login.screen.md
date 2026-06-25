# Login Screen

## API
POST `/api/v1/auth/login`

## Request
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `username` | string | yes | 1-100 chars |
| `password` | string | yes | min 1 char |
| `X-Device-Token` | header | no | string, for device tracking |

## Response (200)
```json
{
  "access_token": "string",
  "refresh_token": "string"
}
```

## Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

## Screen States

### Idle
- Clean form with two fields: username, password
- Submit button ("Sign In")
- Link to forgot-password screen
- Optionally, a "Remember me" checkbox

### Loading
- Submit button shows spinner, fields disabled
- "Signing in..." text on button

### Success
- Store `access_token` and `refresh_token` securely
- Redirect user to main app screen (dashboard/home)

### Error — Validation (422)
- Highlight invalid fields with red border
- Show error message below each invalid field
- Show summary error banner at top of form if needed
- Clear errors on field change

### Error — Network / Server Error
- Generic error banner: "Unable to sign in. Please try again."
- Fields remain editable
- No destructive state loss

### Error — Invalid Credentials
- Show inline error above submit button: "Invalid username or password"
- Do NOT reveal which field is incorrect (security)
