"""
Strategy Design Pattern

Intent:
- Define a family of algorithms.
- Encapsulate each algorithm in a separate class.
- Make them interchangeable at runtime.

Interview example:
- Checkout service can use UPI, credit card, or debit card payment strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Strategy interface."""

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class UPIPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid Rs. {amount} using UPI")


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid Rs. {amount} using Credit Card")


class DebitCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid Rs. {amount} using Debit Card")


class CheckoutService:
    """Context class that works with any payment strategy."""

    def __init__(self, payment_strategy: PaymentStrategy) -> None:
        self.payment_strategy = payment_strategy

    def checkout(self, amount: float) -> None:
        print(f"Processing order for Rs. {amount}")
        self.payment_strategy.pay(amount)


if __name__ == "__main__":
    checkout_service = CheckoutService(UPIPayment())
    checkout_service.checkout(1200)

    checkout_service.payment_strategy = CreditCardPayment()
    checkout_service.checkout(2500)

    checkout_service.payment_strategy = DebitCardPayment()
    checkout_service.checkout(1800)
