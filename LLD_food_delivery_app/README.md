# Food Delivery App - Low Level Design (LLD)

This document describes the LLD for a food delivery system based on your UML.

## Scope

The design covers:
- Restaurant discovery
- Cart operations
- Order creation via factory
- Order type polymorphism (`DeliveryOrder`, `PickupOrder`)
- Payment via strategy pattern
- Global order tracking/management
- Notification trigger after order events

## Core Requirements

- User can browse restaurants and menus.
- User can add menu items into cart.
- User can place order as:
  - Immediate order
  - Scheduled order
- Order can be:
  - Delivery
  - Pickup
- User can choose payment mode (UPI, NetBanking, etc.).
- System stores placed orders in central manager.
- Notification service sends order update.

## Design Patterns Used

- **Singleton**
  - `RestaurantManager`
  - `OrderManager`
- **Factory Method**
  - `OrderFactory` -> `NowOrderFactory`, `ScheduledOrderFactory`
- **Strategy**
  - `PaymentStrategy` -> concrete payment strategies (`UPI`, `NetBanking`)
- **Model/Entity objects**
  - `User`, `Cart`, `Restaurant`, `MenuItem`, `Order`

## Class Responsibilities

## `MenuItem`
- Represents an item in a restaurant menu.
- Fields:
  - `code: int`
  - `name: str`
  - `price: float`

## `Restaurant`
- Represents a restaurant and its menu.
- Fields:
  - `id: int`
  - `name: str`
  - `address: str`
  - `menu_items: List[MenuItem]`

## `RestaurantManager` (Singleton)
- Owns restaurant collection and discovery APIs.
- Fields:
  - `restaurants: List[Restaurant]`
- Methods:
  - `add_restaurant(restaurant)`
  - `search_by_location(location)`
  - CRUD methods (as in your UML notes)

## `Cart`
- User-specific temporary order container.
- Fields:
  - `restaurant: Restaurant`
  - `items: List[MenuItem]`
  - `total: float`
- Methods:
  - `add_to_cart(item)`
  - `clear()`
  - `is_empty()`

## `User`
- Represents app user.
- Fields:
  - `id: int`
  - `name: str`
  - `address: str`
  - `cart: Cart`

## `Order` (Abstract)
- Shared order abstraction.
- Fields:
  - `id: int`
  - `restaurant: Restaurant`
  - `items: List[MenuItem]`
  - `user: User`
  - `payment_strategy: PaymentStrategy`
- Methods:
  - `get_type() -> str`

## `DeliveryOrder` / `PickupOrder`
- Concrete order types.
- Override `get_type()`.

## `OrderFactory` (Interface)
- Contract for creating orders.
- Method:
  - `create_order(...) -> Order`

## `NowOrderFactory`
- Creates immediate orders.

## `ScheduledOrderFactory`
- Creates future/scheduled orders.
- Can include schedule validation (`scheduled_at > now`).

## `PaymentStrategy` (Abstract)
- Method:
  - `pay(amount)`

## Concrete Payment Strategies
- `UPI`
- `NetBanking`
- (Extensible: `Card`, `Wallet`, `CashOnDelivery`)

## `OrderManager` (Singleton)
- Centralized order registry.
- Fields:
  - `orders: List[Order]`
- Methods:
  - `add_order(order)`
  - `get_order(order_id)`
  - `list_user_orders(user_id)`

## `NotificationService`
- Sends order notification events.
- Method:
  - `notify(order)`

## Suggested End-to-End Flow

1. User discovers restaurants via `RestaurantManager.search_by_location(...)`.
2. User selects `Restaurant`, adds `MenuItem`s to `Cart`.
3. App picks `OrderFactory` (`NowOrderFactory` or `ScheduledOrderFactory`).
4. Factory creates concrete `Order` (`DeliveryOrder` or `PickupOrder`).
5. `Order.payment_strategy.pay(total_amount)` executes payment.
6. `OrderManager.add_order(order)` persists order in memory/store.
7. `NotificationService.notify(order)` sends confirmation/update.

## Key Relationships

- One `Restaurant` has many `MenuItem`s.
- One `User` owns one `Cart`.
- One `Order` belongs to one `User` and one `Restaurant`.
- One `Order` contains many `MenuItem`s.
- `Order` depends on one `PaymentStrategy`.
- `RestaurantManager` stores many `Restaurant`s.
- `OrderManager` stores many `Order`s.

## Validation Rules (Recommended)

- Cart cannot include items from multiple restaurants in a single order.
- Empty cart cannot be checked out.
- Scheduled order time must be in the future.
- Payment failure should not create confirmed order.
- Pickup order should not require delivery address.

## Extensibility

- Add new payment methods by implementing `PaymentStrategy`.
- Add new order categories (e.g., `GroupOrder`) by extending `Order`.
- Plug persistent repository under managers (`OrderRepository`, `RestaurantRepository`).
- Add status state machine (`CREATED`, `PAID`, `PREPARING`, `OUT_FOR_DELIVERY`, `DELIVERED`, `CANCELLED`).

## Assumptions from Handwritten UML

The image text is partly unclear; these interpretations were applied:
- `OrderFactory` has at least two implementations: now and scheduled.
- Payment examples include `UPI` and `NetBanking`.
- `RestaurantManager` and `OrderManager` are singleton-like controllers.
- `NotificationService.notify(order)` is called after order creation/update.

If you want, I can generate a complete Python skeleton implementation from this same LLD in the same folder.
