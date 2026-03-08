# Order Lifecycle and Sequence Notes

## Checkout Sequence

1. User selects restaurant and items.
2. System validates single-restaurant cart rule.
3. User selects order timing:
   - Immediate -> `NowOrderFactory`
   - Scheduled -> `ScheduledOrderFactory`
4. Factory returns concrete order type (`DeliveryOrder` or `PickupOrder`).
5. Selected payment strategy executes `pay(amount)`.
6. On success, `OrderManager.add_order(order)` persists order.
7. `NotificationService.notify(order)` sends confirmation.

## Failure Handling

- Payment failure:
  - order marked failed/unpaid
  - no final confirmation sent
- Invalid schedule:
  - reject order and show validation message
- Empty cart:
  - reject checkout request

## Suggested Order Statuses

- `CREATED`
- `PAYMENT_PENDING`
- `PAID`
- `PREPARING`
- `READY_FOR_PICKUP` / `OUT_FOR_DELIVERY`
- `COMPLETED`
- `CANCELLED`

## Non-Functional Expectations

- Idempotent payment callbacks.
- Thread-safe singleton initialization.
- Audit logs for order state transitions.
- Retry policy for transient notification failures.
