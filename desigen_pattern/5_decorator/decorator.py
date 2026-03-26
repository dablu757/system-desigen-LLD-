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

'''
Structure
    Component → Base interface
    Concrete Component → Original object
    Decorator → Wraps the object
    Concrete Decorators → Add new behavior
'''

from abc import ABC, abstractmethod

# Component
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

# Concrete Component
class SimpleCoffee(Coffee):
    def cost(self):
        return 5

# Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost()

# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 2

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 1


# Usage
coffee = SimpleCoffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)

print(coffee.cost())  # 8

'''
How It Works
    Start with SimpleCoffee
    Wrap with MilkDecorator
    Wrap again with SugarDecorator
    Each wrapper adds behavior

--------------------------------------
Visual Flow
    SimpleCoffee
         ↓ wrap
    MilkDecorator
        ↓ wrap
    SugarDecorator
         ↓
    Final Coffee (with all features)

--------------------------------------

Where Used in Real World

    FastAPI / Django middleware

    Logging systems

    Authentication wrappers

    Python decorators (@login_required)

    UI enhancements (scroll, border, shadow)

--------------------------------------

Advantages

    Add features at runtime

    Avoid too many subclasses

    Flexible & reusable

    Follows Open/Closed Principle

--------------------------------------

Disadvantages

    Many small classes

    Hard to debug sometimes

--------------------------------------

Interview Tip (Very Important)

Difference from Inheritance:

    Inheritance → fixed at compile time
    Decorator → flexible at runtime

--------------------------------------

Perfect Interview Answer (Use This)

    Decorator pattern wraps an object to dynamically add new behavior without 
    modifying its original class, providing a flexible alternative to inheritance.

'''























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
