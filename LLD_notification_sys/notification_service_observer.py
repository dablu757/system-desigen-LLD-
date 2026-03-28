"""
Notification System - Observer Pattern Version

Use this version when notifications should be triggered automatically
after system events such as order placed, payment failed, or shipment delivered.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Type


@dataclass
class User:
    # Stores contact information and the user's channel preferences.
    user_id: int
    email: str
    phone: str
    preferences: Dict[str, bool] = field(default_factory=dict)


@dataclass
class Notification:
    # Represents the final message to be delivered to a user.
    user: User
    message: str


@dataclass
class NotificationResult:
    # Captures which channels succeeded and which failed during one send attempt.
    sent_channels: List[str] = field(default_factory=list)
    failed_channels: Dict[str, str] = field(default_factory=dict)


@dataclass
class Event:
    # Represents a business event that can trigger notification delivery.
    name: str
    user: User
    message: str


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        """Send the notification using a concrete delivery channel."""


class EmailNotification(NotificationChannel):
    def send(self, notification: Notification) -> None:
        if not notification.user.email:
            raise ValueError("Email address is missing")
        print(f"Sending EMAIL to {notification.user.email}: {notification.message}")


class SMSNotification(NotificationChannel):
    def send(self, notification: Notification) -> None:
        if not notification.user.phone:
            raise ValueError("Phone number is missing")
        print(f"Sending SMS to {notification.user.phone}: {notification.message}")


class PushNotification(NotificationChannel):
    def send(self, notification: Notification) -> None:
        print(
            f"Sending PUSH notification to user {notification.user.user_id}: "
            f"{notification.message}"
        )


class NotificationFactory:
    # Central registry for channel implementations.
    _channels: Dict[str, Type[NotificationChannel]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def get_notification_channel(cls, channel_type: str) -> NotificationChannel:
        channel_class = cls._channels.get(channel_type)
        if channel_class is None:
            raise ValueError(f"Unsupported channel type: {channel_type}")
        return channel_class()


class NotificationService:
    def __init__(self, factory: type[NotificationFactory] = NotificationFactory):
        self.factory = factory

    def send_notification(self, notification: Notification) -> NotificationResult:
        # The service iterates through enabled user preferences and tries each channel.
        result = NotificationResult()

        for channel_type, is_enabled in notification.user.preferences.items():
            if not is_enabled:
                continue

            try:
                notifier = self.factory.get_notification_channel(channel_type)
                notifier.send(notification)
                result.sent_channels.append(channel_type)
            except Exception as exc:
                # Channel failures are isolated so one bad channel does not stop others.
                result.failed_channels[channel_type] = str(exc)

        return result


class Observer(ABC):
    @abstractmethod
    def update(self, event: Event) -> None:
        """React to a published business event."""


class NotificationObserver(Observer):
    # Converts business events into notifications and delegates delivery to the service.
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def update(self, event: Event) -> None:
        notification = Notification(user=event.user, message=event.message)
        result = self.notification_service.send_notification(notification)

        print(f"\nNotification summary for event '{event.name}'")
        print("Sent via:", result.sent_channels)
        print("Failures:", result.failed_channels)


class EventManager:
    def __init__(self) -> None:
        # Keeps a list of subscribers interested in emitted events.
        self.observers: List[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify(self, event: Event) -> None:
        # Broadcast the same event to all subscribed observers.
        for observer in self.observers:
            observer.update(event)


if __name__ == "__main__":
    # Example flow:
    # 1. Create a user and an event source.
    # 2. Subscribe the notification observer.
    # 3. Publish an ORDER_PLACED event.
    user = User(
        user_id=1,
        email="testuser@gmail.com",
        phone="1234567809",
        preferences={"email": True, "sms": True, "push": False},
    )

    event_manager = EventManager()
    notification_service = NotificationService()
    notification_observer = NotificationObserver(notification_service)

    event_manager.subscribe(notification_observer)

    order_placed_event = Event(
        name="ORDER_PLACED",
        user=user,
        message="Your order has been placed successfully.",
    )

    event_manager.notify(order_placed_event)
