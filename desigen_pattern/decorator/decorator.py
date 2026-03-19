"""
Decorator Design Pattern
========================

Definition
----------
Decorator pattern lets you add new behavior to an 
object at runtime without changing its original class.


Real-Life Analogy
-----------------
Think of ordering coffee:
- Start with a plain coffee.
- Add milk.
- Add sugar.
- Add whipped cream.

Each topping adds extra cost and description without changing the original
coffee class.

Interview One-Liner
-------------------
Use Decorator when you want to add responsibilities to objects at runtime
without creating too many subclasses.
"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass


class SimpleCoffee(Coffee):
    def cost(self):
        return 100

    def description(self):
        return "Simple Coffee"


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee


class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 20

    def description(self):
        return self._coffee.description() + ", Milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 10

    def description(self):
        return self._coffee.description() + ", Sugar"


class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 30

    def description(self):
        return self._coffee.description() + ", Whipped Cream"


if __name__ == "__main__":
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)
    coffee = WhippedCreamDecorator(coffee)

    print("Order:", coffee.description())
    print("Total Cost:", coffee.cost())
