"""
Observer Design Pattern

Intent:
- Define a one-to-many dependency between objects.
- When subject state changes, all subscribed observers are notified automatically.

Interview example:
- YouTube channel notifies email and mobile subscribers when a new video is uploaded.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Observer interface."""

    @abstractmethod
    def update(self, message: str) -> None:
        pass


class Subject(ABC):
    """Subject interface."""

    @abstractmethod
    def subscribe(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass


class YouTubeChannel(Subject):
    """Concrete subject that broadcasts updates to all subscribers."""

    def __init__(self, channel_name: str) -> None:
        self.channel_name = channel_name
        self.observers: List[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)

    def upload_video(self, title: str) -> None:
        message = f"{self.channel_name} uploaded a new video: {title}"
        self.notify(message)


class EmailSubscriber(Observer):
    def update(self, message: str) -> None:
        print(f"Email notification: {message}")


class MobileSubscriber(Observer):
    def update(self, message: str) -> None:
        print(f"Mobile notification: {message}")


if __name__ == "__main__":
    channel = YouTubeChannel("CodeWithInterview")

    email_subscriber = EmailSubscriber()
    mobile_subscriber = MobileSubscriber()

    channel.subscribe(email_subscriber)
    channel.subscribe(mobile_subscriber)

    channel.upload_video("Observer Design Pattern Explained")
