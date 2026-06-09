# Approval Queue (Generic Template)

## Purpose

Approve or reject items in a single queue. One template applies to all 15 queues
(3 transaction types × 5 approval stages).

## Routes

| Transaction | Post | Deposit | Cancellation | Closure | Sold-Out |
|-------------|------|---------|-------------|---------|----------|
| BÁN | `/admin/ban/duyet` | `/admin/ban/duyet-bao-coc` | `/admin/ban/duyet-huy-coc` | `/admin/ban/duyet-chot-hang` | `/admin/ban/duyet-het-hang` |
| CHO THUÊ | `/admin/cho-thue/duyet` | `/admin/cho-thue/duyet-bao-coc` | `/admin/cho-thue/duyet-huy-coc` | `/admin/cho-thue/duyet-chot-hang` | `/admin/cho-thue/duyet-het-hang` |
| SANG NHƯỢNG | `/admin/sang-nhuong/duyet` | `/admin/sang-nhuong/duyet-bao-coc` | `/admin/sang-nhuong/duyet-huy-coc` | `/admin/sang-nhuong/duyet-chot-hang` | `/admin/sang-nhuong/duyet-het-hang` |

## Components

### Queue Header
- Queue name (e.g., "Duyệt bài đăng — BÁN")
- Pending count

### Item List (table/grid)
Each item shows:
- Listing title (linked to product detail)
- Product code
- Agent name
- Submitted date
- Status-specific details:
  - Deposit: customer name, phone, amount
  - Closure/cancellation/sold-out: reporter name, notes

### Action Buttons (per item)
- "Approve" — opens confirmation dialog (optional reason)
- "Reject" — opens reason dialog (required)

### Filters
- By date range
- By agent (if applicable)

### Multi-Select
- Bulk approve (for listing post approvals)

## Entities

- Listing
- Approval
- DealEvent

## Related Stories

- Approval Workflow US-001 (approve), US-002 (reject), US-003 (bulk approve)

## Navigation Links

- Product Detail `/san-pham/:id` (via listing click)
- Shared Cart Home `/`
- Other admin pages via sidebar
