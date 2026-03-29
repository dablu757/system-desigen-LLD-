"""
Singleton Design Pattern

Intent:
- Ensure only one instance of a class exists.
- Provide a global access point to that single instance.

Interview example:
- App configuration manager shared across the application.
"""

from __future__ import annotations

from threading import Lock, Thread


class AppConfig:
    """Thread-safe singleton implementation."""

    _instance: "AppConfig | None" = None
    _lock = Lock()

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.environment = "dev"
                    cls._instance.debug = True
        return cls._instance

    def show(self) -> None:
        print(
            f"AppConfig(environment={self.environment}, debug={self.debug})"
        )


def create_config_instance() -> None:
    config = AppConfig()
    print(f"Instance id: {id(config)}")


if __name__ == "__main__":
    config_1 = AppConfig()
    config_2 = AppConfig()

    config_1.show()
    print("Same instance:", config_1 is config_2)

    print("\nThread-safe check:")
    threads = [Thread(target=create_config_instance) for _ in range(3)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
