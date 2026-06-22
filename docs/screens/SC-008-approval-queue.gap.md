# Gap Analysis: SC-008 Approval Queue

## Against: openapi.yaml

---

## Missing Fields

### 1. Deposit-specific details in queue items
- **Screen**: Deposit queue items show "customer name, phone, amount"
- **Schema**: `ApprovalQueueItem` embeds only `Listing` — no customer info
- **Source data**: `DealEvent` stores `customerName`, `customerPhone`, `depositAmount` (DE-C01)
- **Impact**: Deposit queue renders empty fields for customer data
- **Fix**: Add `dealEvent: DealEvent` (nullable) to `ApprovalQueueItem`, populated only for deposit/closure/cancellation/sold-out queue types

### 2. Reporter name in non-deposit queues
- **Screen**: Closure/cancellation/sold-out items show "reporter name, notes"
- **Schema**: `ApprovalQueueItem` has no reporter info
- **Source data**: `DealEvent.reportedById` (UUID) — needs user lookup
- **Impact**: Cannot display who reported the event without extra API call
- **Fix**: Add `reportedBy: { id: uuid, fullName: string }` to `ApprovalQueueItem`

### 3. Status-specific notes
- **Screen**: Each queue item shows "reporter name, notes" in context
- **Schema**: No notes field in `ApprovalQueueItem`
- **Impact**: Notes from `DealEvent.notes` not accessible in queue view
- **Fix**: Include `notes: string` in `ApprovalQueueItem` when relevant

## Missing API Params

### 1. No date-range filter
- **Screen**: "By date range" filter option
- **API**: `GET /approvals/queues/{queueType}` accepts only `transactionType`, `page`, `size`
- **Impact**: Cannot filter old items out of the queue view
- **Fix**: Add optional `createdAfter` (date-time) and `createdBefore` (date-time) query params

### 2. No agent filter
- **Screen**: "By agent" filter option
- **API**: No `reportedById` or `createdById` filter on queue endpoint
- **Impact**: Cannot narrow queue to a specific agent's submissions
- **Fix**: Add optional `agentId` (UUID) query param

## Inconsistent Naming

### 1. Frontend routes vs API parameterization
- **Screen**: 15 individual routes (`/admin/ban/duyet`, `/admin/cho-thue/duyet-bao-coc`, etc.)
- **API**: Single parameterized endpoint: `GET /approvals/queues/{queueType}?transactionType=BAN`
- **Status**: The FE must map routes to API params. Document the mapping:

| FE Route | queueType | transactionType |
|----------|-----------|-----------------|
| `/admin/ban/duyet` | `listing-post` | `BAN` |
| `/admin/cho-thue/duyet` | `listing-post` | `CHO_THUE` |
| `/admin/sang-nhuong/duyet` | `listing-post` | `SANG_NHUONG` |
| `/admin/ban/duyet-bao-coc` | `deposit` | `BAN` |
| ... | ... | ... |
- **Fix**: This is acceptable; the mapping should be documented in the API spec or FE config

## Resolved Gaps

| Gap | Implementation | Item |
|-----|---------------|------|
| Deposit-specific details (customer name, phone, amount) | `DealEventInfo` schema with `customerName`, `customerPhone`, `depositAmount`, `notes`; `deal_event` field on `QueueItemResponse`, populated only for deposit/closure/cancellation/sold-out queue types | 2.9 |
| Reporter name | `ReporterInfo` schema with `id`, `fullName`; `reported_by` field on `QueueItemResponse`; added `reported_by` relationship to `DealEventEntity` | 2.9 |
| Status-specific notes | Available via `DealEventInfo.notes` on `deal_event` field | 2.9 |
| No date-range filter | `date_from` (alias `dateFrom`) and `date_to` (alias `dateTo`) params on `GET /approvals/queues/{queueType}` | 3.1 |
| No agent filter | `agent_id` (alias `agentId`, UUID) param on `GET /approvals/queues/{queueType}` — filters by `DealEvent.reportedById` or `Listing.createdById` depending on queue type | 3.1 |

## Validated (No Gap)

| Screen Element | API Match | Status |
|----------------|-----------|--------|
| Queue header + pending count | `GET /approvals/queues` → `pendingCount` | ✓ |
| Listing card in queue item | `ApprovalQueueItem.listing` | ✓ |
| Product code | `Listing.code` | ✓ |
| Submitted date | `Listing.createdAt` | ✓ |
| Cover image | `Listing.images` via detail endpoint | ✓ |
| Approve action | `POST /approvals/{id}/approve` | ✓ |
| Reject action with reason | `POST /approvals/{id}/reject` with `RejectRequest.reason` | ✓ |
| Bulk approve | `POST /approvals/bulk-approve` | ✓ |
| Access control (Admin only) | `security: BearerAuth` + `403 Forbidden` for non-Admin | ✓ |
