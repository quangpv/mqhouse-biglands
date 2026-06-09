# Product Overview

## Product Purpose

Biglands is a B2B internal marketplace platform for real estate agents and
brokers specializing in CHDV (Căn Hộ Dịch Vụ — serviced apartment buildings)
in Ho Chi Minh City. It functions as a shared deal pool ("giỏ hàng chung")
where agents list, discover, transact, and coordinate on CHDV properties.

The platform replaces fragmented communication (Zalo, phone, spreadsheets)
with a structured pipeline: listing → deposit → deal closure → sold-out.

## Target Users

- Sales agents and brokers dealing in CHDV properties
- Real estate team leaders / brokerage managers
- Admin operations staff
- System administrators

## User Roles

| Role | Capabilities |
|------|-------------|
| **Agent** | Browse shared cart, create/edit own listings, report deposits, report sold-out/deal closure/cancellation on own listings |
| **Approver** | All Agent capabilities + approve/reject listings, deposits, cancellations, closures, and sold-out status across one or more transaction categories |
| **Admin** | All Approver capabilities + manage users, manage hot products, manage system notifications |

## Main Workflows

1. **Listing Lifecycle**: Agent creates listing → Approver reviews → Listing goes live → Agents market to customers
2. **Deposit-to-Deal Pipeline**: Customer deposits → Agent reports deposit → Approver confirms → Deal closes or gets cancelled
3. **Sold-Out Flow**: Agent reports property as sold → Approver confirms → Listing removed from active pool

## Site Map

```
Home (Shared Cart)
├── Product Detail
│   ├── Report Deposit
│   ├── Report Deal Closure
│   ├── Report Cancellation
│   └── Report Sold-Out
├── My Cart (Personal)
├── Create Listing
├── Notifications
└── Admin Panel
    ├── Hot Products
    ├── User Management
    ├── Sell Approval Queue
    │   ├── Approve Listings
    │   ├── Approve Deposits
    │   ├── Approve Cancellations
    │   ├── Approve Closures
    │   └── Approve Sold-Out
    ├── Rent Approval Queue (same 5 queues)
    └── Transfer Approval Queue (same 5 queues)
```

## Feature Inventory

| Category | Features |
|----------|----------|
| **Browsing** | Product grid with cards, pagination, search by keyword/address/code, filter tabs: All (Tất cả loại hàng), Pinned (Đã ghim), Hot (Hàng Hot) |
| **Listing Mgmt** | Create listing, edit listing, change status, upload images, set attributes (rooms, area, price, etc.) |
| **Approval** | 3 categories × 5 stages = 15 approval queues; approve/reject with reason |
| **Deal Ops** | Report deposit, approve deposit, report closure, report cancellation, mark sold-out |
| **User Admin** | Create/edit/deactivate users, assign roles |
| **Notifications** | Receive alerts on approval requests, status changes; read/unread |
| **Hot Products** | Promote listings to "hot" badge; manage hot list order |

## Domain Overview

Biglands deals exclusively with CHDV (serviced apartment buildings) — entire
buildings, not individual units. Properties are listed in three transaction modes:

- **SANG NHƯỢNG**: Transfer of leasehold/business rights of an operating CHDV
- **CHO THUÊ**: Rental of the entire building
- **BÁN**: Outright sale of the property

Each transaction type has an independent approval pipeline.

## Listing Title Conventions

Listing titles commonly use Vietnamese real-estate abbreviations as prefixes:

| Prefix | Full Term | Meaning |
|--------|-----------|---------|
| **NNC** | Nhà Nguyên Căn | Entire building/house (not individual units) |
| **MT** | Mặt Tiền | Street-fronting property |
| **HXH** | Hẻm Xe Hơi | Car-accessible alley |
| **CHDV** | Căn Hộ Dịch Vụ | Serviced apartment building |

These prefixes classify the property type/position and appear at the start of the listing title.
