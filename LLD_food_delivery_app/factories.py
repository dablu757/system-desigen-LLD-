from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime

from LLD_food_delivery_app.models import DeliveryOrder, MenuItem, Order, PickupOrder, Restaurant, User
from LLD_food_delivery_app.strategies import PaymentStrategy


class OrderFactory(ABC):
    """Factory method contract for creating orders."""

    @abstractmethod
    def create_order(
        self,
        order_id: int,
        user: User,
        restaurant: Restaurant,
        items: list[MenuItem],
        payment_strategy: PaymentStrategy,
        order_type: str,
        scheduled_at: datetime | None = None,
    ) -> Order:
        pass


class NowOrderFactory(OrderFactory):
    def create_order(
        self,
        order_id: int,
        user: User,
        restaurant: Restaurant,
        items: list[MenuItem],
        payment_strategy: PaymentStrategy,
        order_type: str,
        scheduled_at: datetime | None = None,
    ) -> Order:
        if scheduled_at is not None:
            raise ValueError("NowOrderFactory does not accept scheduled_at")

        kind = order_type.strip().lower()
        if kind == "delivery":
            return DeliveryOrder(
                id=order_id,
                restaurant=restaurant,
                items=items,
                user=user,
                payment_strategy=payment_strategy,
                delivery_address=user.address,
            )
        if kind == "pickup":
            return PickupOrder(
                id=order_id,
                restaurant=restaurant,
                items=items,
                user=user,
                payment_strategy=payment_strategy,
                pickup_time=datetime.now(UTC),
            )
        raise ValueError(f"Unsupported order_type: {order_type}")


class ScheduledOrderFactory(OrderFactory):
    def create_order(
        self,
        order_id: int,
        user: User,
        restaurant: Restaurant,
        items: list[MenuItem],
        payment_strategy: PaymentStrategy,
        order_type: str,
        scheduled_at: datetime | None = None,
    ) -> Order:
        if scheduled_at is None:
            raise ValueError("scheduled_at is required for scheduled orders")
        if scheduled_at <= datetime.now(UTC):
            raise ValueError("scheduled_at must be in the future")

        kind = order_type.strip().lower()
        if kind == "delivery":
            return DeliveryOrder(
                id=order_id,
                restaurant=restaurant,
                items=items,
                user=user,
                payment_strategy=payment_strategy,
                delivery_address=user.address,
            )
        if kind == "pickup":
            return PickupOrder(
                id=order_id,
                restaurant=restaurant,
                items=items,
                user=user,
                payment_strategy=payment_strategy,
                pickup_time=scheduled_at,
            )
        raise ValueError(f"Unsupported order_type: {order_type}")
