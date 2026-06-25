# System Configuration

## Overview

Admin-only configuration screen for managing platform settings. Consists of 3 tabs.

**Route:** `/cau-hinh-he-thong`

**Access:** Admin only.

---

## Page Layout

- Page title: "Cấu hình hệ thống" (System Configuration)
- Three tabs to switch between data groups:
  1. **Organizations** (shown by default)
  2. **Transaction Types**
  3. **Property Types**
- Each tab has its own data table.
- All add/edit/delete operations use pop-up dialogs.

---

## Tab 1 — Organizations

### Purpose
Manage the list of organizations (companies, units) using the system.

### Actions

#### View organization list
Table displays:
- #
- Name
- Display Name
- Granted Transaction Types
- Granted Property Types
- Created Date
- Actions (Edit / Delete)

20 organizations per page, with pagination for more.

#### Add new organization
1. Click **"Add Organization"** button at the top right.
2. A pop-up appears with the following fields:
   - **Name**: internal identifier (e.g. `org_biglands`)
   - **Display Name**: name shown in the UI (e.g. Biglands Corp)
   - **Transaction Types**: select one or more types from the available list
   - **Property Types**: select one or more types from the available list
3. Click **"Create Organization"** to save.

#### Edit organization
1. Click the Edit button (pencil icon) on the corresponding row.
2. A pop-up appears with pre-filled data, ready for changes.
3. Click **"Save Changes"** to update.

#### Delete organization
1. Click the Delete button (trash icon) on the corresponding row.
2. A confirmation pop-up appears: *"Are you sure you want to delete organization [name]? This action cannot be undone."*
3. Click **"Delete"** to confirm or **"Cancel"** to discard.

### Screen States

| State | Description |
|-------|-------------|
| **Idle** | Data table displayed with action buttons |
| **Loading** | Table shows grey shimmer skeleton; no actions available |
| **Empty** | Icon + message "No organizations yet" + "Add Organization" button |
| **Validation Error** | Pop-up stays open; invalid fields highlighted in red with error messages |
| **Network Error** | Toast notification: "Unable to connect to server" |
| **Delete Blocked** | Toast notification: "Cannot delete this organization — there are users referencing it" |

---

## Tab 2 — Transaction Types

### Purpose
Manage the list of real estate transaction types (Sell, Rent, Sublease, etc.).

### Actions

#### View list
Table displays:
- #
- Code
- Display Name
- Created Date
- Actions (Edit / Delete)

#### Add new transaction type
1. Click **"Add Transaction Type"** button.
2. Pop-up with fields:
   - **Code**: system code, lowercase, no accents (e.g. `sell`, `rent`)
   - **Display Name**: Vietnamese name shown in the UI (e.g. Bán, Cho thuê)
3. Click **"Create Transaction Type"** to save.

#### Edit / Delete
- Edit: click Edit button, modify details, click **"Save Changes"**.
- Delete: click Delete button, confirm, click **"Delete"**.

### Screen States

Same as Tab 1 (Idle / Loading / Empty / Validation Error / Network Error).

**Special — Delete Blocked:**
- If the transaction type is referenced by an organization, it cannot be deleted.
- Toast shows: *"Cannot delete this transaction type — it is currently in use by an organization"*

---

## Tab 3 — Property Types

### Purpose
Manage the list of real estate property types (Apartment, Townhouse, Land, etc.).

### Actions

#### View list
Table displays:
- #
- Code
- Display Name
- Created Date
- Actions (Edit / Delete)

#### Add new property type
1. Click **"Add Property Type"** button.
2. Pop-up with fields:
   - **Code**: system code, lowercase, no accents (e.g. `apartment`, `house`)
   - **Display Name**: Vietnamese name shown in the UI (e.g. Căn hộ, Nhà phố)
3. Click **"Create Property Type"** to save.

#### Edit / Delete
- Edit: click Edit button, modify, click **"Save Changes"**.
- Delete: click Delete button, confirm, click **"Delete"**.

### Screen States

**Special — Delete Blocked:**
- If the property type is referenced by an organization, it cannot be deleted.
- Toast shows: *"Cannot delete this property type — it is currently in use by an organization"*

---

## General Rules

### Tab Switching
- Each tab loads its data independently.
- The first switch shows a loading effect; subsequent switches use cached data and are faster.

### Data Load Error
- If a tab fails to load, a *"Failed to load data"* message appears with a **"Retry"** button.

### Delete Protection
- An Organization cannot be deleted if it still has users assigned to it.
- A Transaction Type or Property Type cannot be deleted if it is referenced by an Organization.
- The system shows a specific reason when a delete is blocked.
