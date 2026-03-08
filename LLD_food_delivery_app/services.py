from __future__ import annotations

from dataclasses import dataclass

from LLD_food_delivery_app.models import Order, Restaurant


class RestaurantManager:
    """Singleton manager for restaurant catalog operations."""

    _instance: "RestaurantManager | None" = None

    def __new__(cls) -> "RestaurantManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.restaurants = []
        return cls._instance

    def add_restaurant(self, restaurant: Restaurant) -> None:
        self.restaurants.append(restaurant)

    def search_by_location(self, location: str) -> list[Restaurant]:
        key = location.strip().lower()
        return [r for r in self.restaurants if key in r.address.lower()]


class OrderManager:
    """Singleton manager for orders."""

    _instance: "OrderManager | None" = None

    def __new__(cls) -> "OrderManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.orders = []
        return cls._instance

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def get_order(self, order_id: int) -> Order:
        for order in self.orders:
            if order.id == order_id:
                return order
        raise ValueError(f"Order not found: {order_id}")

    def list_user_orders(self, user_id: int) -> list[Order]:
        return [o for o in self.orders if o.user.id == user_id]


@dataclass(slots=True)
class NotificationService:
    def notify(self, order: Order) -> None:
        print(
            f"Notify user={order.user.id}: Order {order.id} ({order.get_type()}) confirmed"
        )
