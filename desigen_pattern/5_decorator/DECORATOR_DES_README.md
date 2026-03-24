# Decorator Pattern in Python

This module demonstrates the Decorator design pattern using a coffee ordering
example.

Source file: `desigen_pattern/decorator/decorator.py`

## Intent

Attach additional responsibilities to an object dynamically without modifying
its original class.

## Real-Life Analogy

Think of a coffee shop:

- Start with a plain coffee
- Add milk
- Add sugar
- Add whipped cream

Each addon increases the cost and changes the final description, but the base
coffee class stays unchanged.

## Participants

### 1) Component

Defines the common interface for both concrete objects and decorators.

In this code:
- `Coffee`

It exposes:
- `cost()`
- `description()`

### 2) Concrete Component

The base object to which additional behavior can be added.

In this code:
- `SimpleCoffee`

### 3) Decorator

Wraps a component object and follows the same interface.

In this code:
- `CoffeeDecorator`

### 4) Concrete Decorators

Add new behavior or state to the wrapped object.

In this code:
- `MilkDecorator`
- `SugarDecorator`
- `WhippedCreamDecorator`

## Flow

1. Create the base object.
2. Wrap it with one decorator.
3. Wrap it again with more decorators as needed.
4. Each decorator adds its own behavior while delegating to the wrapped object.

## When to Use

- When you want to add features dynamically at runtime
- When subclass explosion becomes a problem
- When you want flexible combinations of features
- In UI components, streams, logging, and middleware-like systems

## Advantages

- Follows Open/Closed Principle
- Avoids too many subclasses
- Features can be combined dynamically
- Each decorator has a single responsibility

## Disadvantages

- Can create many small classes
- Debugging can be harder because objects are wrapped in layers
- The order of decorators can affect behavior

## Decorator vs Inheritance

- **Inheritance**:
  - Adds behavior statically at class level
  - Can lead to many subclasses

- **Decorator**:
  - Adds behavior dynamically at object level
  - More flexible than inheritance

In short:
- Inheritance = compile/design-time extension
- Decorator = runtime extension

## Interview Tip

If the interviewer asks why Decorator is used instead of subclassing:

- Subclassing creates too many combinations such as
  `CoffeeWithMilkSugar`, `CoffeeWithMilkCream`, and so on.
- Decorator avoids this by wrapping objects dynamically.

## Example Output

```text
Order: Simple Coffee, Milk, Sugar, Whipped Cream
Total Cost: 160
```

## Summary

The Decorator pattern is best when you want to extend object behavior
dynamically and flexibly without modifying existing code.
