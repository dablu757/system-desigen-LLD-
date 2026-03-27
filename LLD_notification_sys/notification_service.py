"""
Notification System

Interview talking points:
- Strategy Pattern: each notification channel has its own send() behavior
- Factory Pattern: channel creation is centralized
- Service Layer: business flow stays separate from object creation

This version is intentionally interview-friendly:
- cleaner entities using dataclasses
- extensible factory registry instead of if/elif chains
- per-channel error handling
- result tracking for sent / failed channels
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


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        """Send the notification via the concrete channel."""


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
    def register_channel(
        cls, channel_type: str, channel_class: Type[NotificationChannel]
    ) -> None:
        cls._channels[channel_type] = channel_class

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


if __name__ == "__main__":
    user = User(
        user_id=1,
        email="testuser@gmail.com",
        phone="1234567809",
        preferences={"email": True, "sms": True, "push": False},
    )

    notification = Notification(
        user=user,
        message="Testing notification service",
    )

    notification_service = NotificationService()
    result = notification_service.send_notification(notification)

    print("\nSummary")
    print("Sent via:", result.sent_channels)
    print("Failures:", result.failed_channels)
