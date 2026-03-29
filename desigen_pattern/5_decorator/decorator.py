"""
Decorator Design Pattern

Intent:
- Add new behavior to an object dynamically at runtime.
- Avoid creating too many subclasses for every feature combination.

Interview example:
- Build a coffee order and keep adding milk, sugar, and whipped cream.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Coffee(ABC):
    """Component interface."""

    @abstractmethod
    def cost(self) -> int:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class SimpleCoffee(Coffee):
    """Concrete component."""

    def cost(self) -> int:
        return 100

    def description(self) -> str:
        return "Simple Coffee"


class CoffeeDecorator(Coffee):
    """Base decorator that wraps another coffee object."""

    def __init__(self, coffee: Coffee) -> None:
        self.coffee = coffee


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> int:
        return self.coffee.cost() + 20

    def description(self) -> str:
        return f"{self.coffee.description()}, Milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> int:
        return self.coffee.cost() + 10

    def description(self) -> str:
        return f"{self.coffee.description()}, Sugar"


class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self) -> int:
        return self.coffee.cost() + 30

    def description(self) -> str:
        return f"{self.coffee.description()}, Whipped Cream"


if __name__ == "__main__":
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)
    coffee = WhippedCreamDecorator(coffee)

    print("Order:", coffee.description())
    print("Total Cost:", coffee.cost())
