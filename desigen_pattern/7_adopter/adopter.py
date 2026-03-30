"""
Adapter Design Pattern

Definition:
- Adapter converts one interface into another interface that the client expects.
- It works like a translator between incompatible classes.

Interview flow:
Client -> Target Interface -> Adapter -> Adaptee

Common interview example:
- Your app expects a standard payment processor interface.
- A third-party gateway exposes a different method signature.
- Adapter helps both work together without changing client code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


#target interface expected by the client
class PaymentProcessor(ABC):
    """Target interface expected by the client code."""

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


#third party service with its own incompatible
class StripeGateway:
    """Existing third-party service with its own incompatible API."""

    def make_payment(self, amount_in_rupees: float) -> None:
        print(f"Stripe payment of Rs. {amount_in_rupees} completed")
class PayPalGateway:
    """Another third-party service with a different method name."""

    def send_money(self, value: float) -> None:
        print(f"PayPal payment of Rs. {value} completed")



#adapter connvert client call into third party gateway
class StripeAdapter(PaymentProcessor):
    """Adapter converts client calls into StripeGateway calls."""

    def __init__(self, stripe_gateway: StripeGateway) -> None:
        self.stripe_gateway = stripe_gateway

    def pay(self, amount: float) -> None:
        self.stripe_gateway.make_payment(amount)
class PayPalAdapter(PaymentProcessor):
    """Adapter converts client calls into PayPalGateway calls."""

    def __init__(self, paypal_gateway: PayPalGateway) -> None:
        self.paypal_gateway = paypal_gateway

    def pay(self, amount: float) -> None:
        self.paypal_gateway.send_money(amount)


#client class 
class CheckoutService:
    """
    Client class.
    It only depends on the standard PaymentProcessor interface
    and does not care which gateway is actually used underneath.
    """

    def __init__(self, payment_processor: PaymentProcessor) -> None:
        self.payment_processor = payment_processor

    def checkout(self, amount: float) -> None:
        print(f"Initiating checkout for Rs. {amount}")
        self.payment_processor.pay(amount)
        print("Order placed successfully")


#client call

if __name__ == "__main__":
    stripe_gateway = StripeGateway()
    stripe_adapter = StripeAdapter(stripe_gateway)
    stripe_checkout = CheckoutService(stripe_adapter)
    stripe_checkout.checkout(2500)

    print()

    paypal_gateway = PayPalGateway()
    paypal_adapter = PayPalAdapter(paypal_gateway)
    paypal_checkout = CheckoutService(paypal_adapter)
    paypal_checkout.checkout(1800)
