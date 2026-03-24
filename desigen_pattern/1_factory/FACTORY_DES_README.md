# Factory Patterns in Python

This module demonstrates three creation patterns using a burger restaurant example:

- Simple Factory
- Factory Method
- Abstract Factory

Source file: `desigen_pattern/factory_desigen_pattern.py`

## 1) Simple Factory

### Intent
Centralize object creation in one place so client code does not instantiate concrete classes directly.

### In this code
- Product interface: `SimpleBurger`
- Concrete products: `BasicBurger`, `StandardBurger`, `PremiumBurger`
- Factory: `SimpleBurgerFactory`

`SimpleBurgerFactory.create_burger(burger_type)` uses a dictionary map (`_burger_map`) to return the correct burger class.

## 2) Factory Method

### Intent
Define an interface for object creation, letting subclasses decide which concrete product to build.

### In this code
- Product interface: `Burger`
- Concrete products (Regular family):
  - `RegularBasicBurger`, `RegularStandardBurger`, `RegularPremiumBurger`
- Concrete products (Wheat family):
  - `WheatBasicBurger`, `WheatStandardBurger`, `WheatPremiumBurger`
- Creator (abstract): `BurgerFactory`
- Concrete creators:
  - `SinghBurgerFactory` (creates Wheat burgers)
  - `KingBurgerFactory` (creates Regular burgers)

Each concrete factory implements `create_burger(burger_type)` and uses its own `_burger_map`.

## 3) Abstract Factory

### Intent
Create families of related objects without specifying concrete classes in client code.

### In this code
- Abstract products: `Burger`, `Drink`
- Concrete product families:
  - Regular: `RegularBurger`, `RegularDrink`
  - Wheat: `WheatBurger`, `WheatDrink`
- Abstract factory: `RestaurantFactory`
- Concrete factories:
  - `SinghRestaurantFactory` -> `RegularBurger` + `RegularDrink`
  - `KingRestaurantFactory` -> `WheatBurger` + `WheatDrink`
- Client function: `serve_customer(factory)`

The client only depends on `RestaurantFactory`, not concrete classes.

## How to Run

From project root:

```bash
python desigen_pattern/factory_desigen_pattern.py
```

Expected output:

```text
Singh Restaurant Order
Preparing Regular Burger
Serving Regular Cold Drink
----------------------------------------
King Restaurant Order
Preparing Wheat Burger
Serving Healthy Wheat Smoothie
----------------------------------------
```

## Pattern Comparison

- **Simple Factory**: one class decides all product creation with condition/map logic.
- **Factory Method**: creation responsibility moves to subclasses through polymorphism.
- **Abstract Factory**: creates multiple related products as a compatible family.

## Notes

- Invalid burger type values raise `ValueError` in simple/factory-method implementations.
- Current naming in code maps `SinghBurgerFactory` to wheat burgers and `KingBurgerFactory` to regular burgers; this is valid as long as it is intentional.
