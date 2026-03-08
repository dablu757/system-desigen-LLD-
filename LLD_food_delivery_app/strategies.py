from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Strategy interface for payment methods."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Return True on successful payment."""


class UPI(PaymentStrategy):
    def __init__(self, upi_id: str) -> None:
        self.upi_id = upi_id

    def pay(self, amount: float) -> bool:
        print(f"UPI payment of {amount:.2f} using {self.upi_id}")
        return True


class NetBanking(PaymentStrategy):
    def __init__(self, bank_name: str) -> None:
        self.bank_name = bank_name

    def pay(self, amount: float) -> bool:
        print(f"NetBanking payment of {amount:.2f} via {self.bank_name}")
        return True
