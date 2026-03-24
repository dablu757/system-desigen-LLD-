"""
Strategy Design Pattern
=======================

Definition
----------
The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable at runtime.

Real-Life Analogy
-----------------
Think of a payment system:
- A customer wants to pay for an order.
- The payment can happen through UPI, Debit Card, or Credit Card.
- The checkout flow remains the same, only the payment method changes.

Interview One-Liner
-------------------
Use Strategy when you have multiple ways to perform the same task and want to
switch behavior dynamically without changing the client code.
"""

from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self):
        pass


class UpiPayment(Payment):
    def pay(self):
        print("This is UPI payment method")


class CreditCardPayment(Payment):
    def pay(self):
        print("This is Credit Card payment method")


class DebitCardPayment(Payment):
    def pay(self):
        print("This is Debit Card payment method")


class PaymentService:
    def __init__(self, payment: Payment):
        self._payment = payment

    def pay(self):
        self._payment.pay()


if __name__ == "__main__":
    payment_services = [
        PaymentService(UpiPayment()),
        PaymentService(DebitCardPayment()),
        PaymentService(CreditCardPayment()),
    ]

    for service in payment_services:
        service.pay()
