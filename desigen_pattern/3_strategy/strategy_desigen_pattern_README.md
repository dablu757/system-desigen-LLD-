# Strategy Design Pattern in Python

This module demonstrates the Strategy design pattern using a payment method
example.

Source file: `desigen_pattern/3_strategy/strategy_desigen_pattern.py`

## Intent

Define a family of algorithms, encapsulate each one, and make them
interchangeable so the client can change behavior at runtime.

## Real-Life Analogy

Think of a payment checkout:

- Customer selects a payment method
- It can be UPI, Debit Card, or Credit Card
- The checkout process remains the same
- Only the algorithm for payment changes

## Participants

### 1) Strategy

Defines the common interface for all algorithms.

In this code:
- `Payment`

It exposes:
- `pay()`

### 2) Concrete Strategies

These classes implement different algorithms.

In this code:
- `UpiPayment`
- `DebitCardPayment`
- `CreditCardPayment`

### 3) Context

The context uses a strategy object instead of hardcoding logic.

In this code:
- `PaymentService`

## Flow

1. Client chooses a strategy object.
2. Strategy object is passed to the context.
3. Context delegates work to the selected strategy.
4. Strategy can be changed without modifying the context.

## When to Use

- When multiple algorithms solve the same problem
- When you want to avoid large if-elif chains
- When behavior should change at runtime
- For payments, sorting, routing, pricing, or discounts

## Advantages

- Replaces conditional logic with polymorphism
- Easy to add new strategies
- Follows Open/Closed Principle
- Improves testing because each strategy is isolated

## Disadvantages

- Adds more classes
- Client must know which strategy to choose
- Can feel heavy for very small problems

## Strategy vs State

- **Strategy**:
  - Client chooses the algorithm
  - Focus is interchangeable behavior

- **State**:
  - Object changes behavior based on internal state
  - Focus is state-driven behavior changes

In short:
- Strategy = behavior selected from outside
- State = behavior changes from inside

## Interview Tip

If the interviewer asks why Strategy is better than `if-else`:

- `if-else` grows large as new behaviors are added
- Strategy keeps each algorithm in its own class
- New behavior can be added without changing existing context code

## Example Output

```text
This is UPI payment method
This is Debit Card payment method
This is Credit Card payment method
```

## Summary

The Strategy pattern is best when you want clean, replaceable, runtime-selectable
algorithms without cluttering the client with conditional logic.
