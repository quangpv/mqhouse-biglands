# User Management CRUD

## Goal

Admin creates, edits, deactivates, or changes roles of platform users.

## Trigger

Admin navigates to User Management from sidebar.

## Preconditions

- User is logged in as Admin

## Main Flow

```mermaid
flowchart TD
    A[Sidebar: Quản lý người dùng] --> B[User list /admin/quan-ly-nguoi-dung]
    B --> C{Choose action}
    
    C -->|Create| D[Click "Create User"]
    D --> E[Fill form: name, username, phone, role]
    E --> F[Submit]
    F --> G[User created, shown in list]
    
    C -->|Edit| H[Click Edit on user row]
    H --> I[Edit form pre-filled]
    I --> J[Modify fields]
    J --> K[Save]
    K --> L[User updated]
    
    C -->|Deactivate| M[Click Deactivate]
    M --> N[Confirm dialog]
    N --> O[User status → Inactive]
    
    C -->|Search| P[Type in search box]
    P --> Q[Filtered results]
```

## Alternative Flows

- **Self-deactivation prevented**: Admin cannot deactivate own account
- **Last admin**: System prevents removing the last ADMIN role
- **Deactivated user login**: Rejected with inactive account error

## Screen References

- SC-009 User Management List
- SC-010 User Create/Edit

## Story References

- User Management US-001 (create), US-002 (edit), US-003 (deactivate), US-004 (assign role)
