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
    user_id: int
    email: str
    phone: str
    preferences: Dict[str, bool] = field(default_factory=dict)


@dataclass
class Notification:
    user: User
    message: str


@dataclass
class NotificationResult:
    sent_channels: List[str] = field(default_factory=list)
    failed_channels: Dict[str, str] = field(default_factory=dict)


@dataclass
class Event:
    name: str
    user: User
    message: str


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        """Send notification via a specific channel."""


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
        result = NotificationResult()

        for channel_type, is_enabled in notification.user.preferences.items():
            if not is_enabled:
                continue

            try:
                notifier = self.factory.get_notification_channel(channel_type)
                notifier.send(notification)
                result.sent_channels.append(channel_type)
            except Exception as exc:
                result.failed_channels[channel_type] = str(exc)

        return result


class Observer(ABC):
    @abstractmethod
    def update(self, event: Event) -> None:
        """React to an emitted event."""


class NotificationObserver(Observer):
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
        self.observers: List[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify(self, event: Event) -> None:
        for observer in self.observers:
            observer.update(event)


if __name__ == "__main__":
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
