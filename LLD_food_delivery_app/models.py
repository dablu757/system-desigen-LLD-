from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional

from LLD_food_delivery_app.strategies import PaymentStrategy


@dataclass(slots=True)
class MenuItem:
    code: int
    name: str
    price: float


@dataclass(slots=True)
class Restaurant:
    id: int
    name: str
    address: str
    menu_items: list[MenuItem] = field(default_factory=list)


@dataclass(slots=True)
class Cart:
    restaurant: Optional[Restaurant] = None
    items: list[MenuItem] = field(default_factory=list)

    def add_to_cart(self, restaurant: Restaurant, item: MenuItem) -> None:
        if self.restaurant is None:
            self.restaurant = restaurant
        if self.restaurant.id != restaurant.id:
            raise ValueError("Cart can contain items from only one restaurant")
        self.items.append(item)

    @property
    def total(self) -> float:
        return sum(item.price for item in self.items)

    def clear(self) -> None:
        self.restaurant = None
        self.items.clear()

    def is_empty(self) -> bool:
        return len(self.items) == 0


@dataclass(slots=True)
class User:
    id: int
    name: str
    address: str
    cart: Cart = field(default_factory=Cart)


@dataclass(slots=True)
class Order(ABC):
    id: int
    restaurant: Restaurant
    items: list[MenuItem]
    user: User
    payment_strategy: PaymentStrategy
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @abstractmethod
    def get_type(self) -> str:
        pass

    @property
    def amount(self) -> float:
        return sum(item.price for item in self.items)


@dataclass(slots=True)
class DeliveryOrder(Order):
    delivery_address: str = ""

    def get_type(self) -> str:
        return "DELIVERY"


@dataclass(slots=True)
class PickupOrder(Order):
    pickup_time: Optional[datetime] = None

    def get_type(self) -> str:
        return "PICKUP"
