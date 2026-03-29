"""
Factory Design Pattern

Intent:
- Create objects without exposing object creation logic to the client.
- Client asks the factory for an object instead of instantiating concrete classes directly.

Interview example:
- Notification system creates Email, SMS, or Push sender objects through a factory.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Type


class Notification(ABC):
    """Product interface."""

    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending EMAIL: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending PUSH: {message}")


class NotificationFactory:
    """Factory that centralizes object creation."""

    _notification_map: Dict[str, Type[Notification]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create_notification(cls, notification_type: str) -> Notification:
        notification_class = cls._notification_map.get(notification_type.lower())
        if notification_class is None:
            raise ValueError(f"Unsupported notification type: {notification_type}")
        return notification_class()


if __name__ == "__main__":
    message = "Your order has been shipped"

    email_sender = NotificationFactory.create_notification("email")
    sms_sender = NotificationFactory.create_notification("sms")
    push_sender = NotificationFactory.create_notification("push")

    email_sender.send(message)
    sms_sender.send(message)
    push_sender.send(message)
