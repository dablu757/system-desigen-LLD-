"""
Command Design Pattern

Intent:
- Encapsulate a request as an object.
- Decouple the invoker from the receiver.
- Support undo/redo, queueing, and request history.

Interview mapping:
- Command: request wrapper
- Receiver: actual business logic
- Invoker: triggers commands
- Client: wires all objects together
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    """Common interface for all commands."""

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    """Receiver that knows how to perform light operations."""

    def turn_on(self) -> None:
        print("Light is ON")

    def turn_off(self) -> None:
        print("Light is OFF")


class Fan:
    """Receiver that knows how to perform fan operations."""

    def start(self) -> None:
        print("Fan is STARTED")

    def stop(self) -> None:
        print("Fan is STOPPED")


class LightOnCommand(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.turn_on()

    def undo(self) -> None:
        self.light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light) -> None:
        self.light = light

    def execute(self) -> None:
        self.light.turn_off()

    def undo(self) -> None:
        self.light.turn_on()


class FanStartCommand(Command):
    def __init__(self, fan: Fan) -> None:
        self.fan = fan

    def execute(self) -> None:
        self.fan.start()

    def undo(self) -> None:
        self.fan.stop()


class FanStopCommand(Command):
    def __init__(self, fan: Fan) -> None:
        self.fan = fan

    def execute(self) -> None:
        self.fan.stop()

    def undo(self) -> None:
        self.fan.start()


class RemoteControl:
    """
    Invoker that executes commands.
    It stores command history to support undo operations.
    """

    def __init__(self) -> None:
        self.history: List[Command] = []

    def submit(self, command: Command) -> None:
        command.execute()
        self.history.append(command)

    def undo_last(self) -> None:
        if not self.history:
            print("No command to undo")
            return

        last_command = self.history.pop()
        last_command.undo()


if __name__ == "__main__":
    # Client code
    light = Light()
    fan = Fan()

    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)
    fan_start = FanStartCommand(fan)
    fan_stop = FanStopCommand(fan)

    remote = RemoteControl()

    print("Executing commands:")
    remote.submit(light_on)
    remote.submit(fan_start)
    remote.submit(light_off)
    remote.submit(fan_stop)

    print("\nUndoing last two commands:")
    remote.undo_last()
    remote.undo_last()
