# ==========================================================
# Singleton Design Pattern
# Ensures only ONE instance of the class is created.
# ==========================================================

'''
__new__ is responsible for object creation, while __init__ initializes it.
In Singleton, we override __new__ to ensure only one instance is created.
cls refers to the class itself and is used to access class-level variables like _instance.
If the instance already exists, we return it instead of creating a new one.
---------------------------------------------------
cls → class reference
__new__() → controls object creation
_instance → stores single instance
super().__new__(cls) → actually creates object
---------------------------------------------------
Short Interview Definition (One Line)
    Singleton ensures that only one object of a class exists throughout 
    the application and provides controlled global access to it.
---------------------------------------------------
Singleton is used in:
    1. Logging systems
    2. Configuration loaders
    3. Database connection managers
    4. Cache managers
    5. Thread pools
    6. Hardware controllers
    7. Application context containers
'''
import threading
class Singleton:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        # First check (NO LOCK)
        if cls._instance is None:

            # Acquire lock only if needed
            with cls._lock:

                # Second check (WITH LOCK)
                if cls._instance is None:
                    print("Creating Singleton instance")
                    cls._instance = super().__new__(cls)

        return cls._instance


# Test
s1 = Singleton()
s2 = Singleton()

print(s1 is s2)















# from __future__ import annotations

# from abc import ABC, ABCMeta, abstractmethod
# from threading import Lock, Thread


# # ==========================================================
# # 1️⃣ CLASSIC SINGLETON (OVERRIDING __new__)
# # ==========================================================
# """
# Classic Singleton:
# - Ensures only one instance of a class exists.
# - Good for shared resources like config/logger/cache.
# """


# class AppConfigSingleton:
#     """
#     Singleton using __new__.
#     All callers get the same instance.
#     """

#     _instance: AppConfigSingleton | None = None

#     def __new__(cls) -> AppConfigSingleton:
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance.env = "dev"
#             cls._instance.debug = True
#         return cls._instance

#     def show(self) -> None:
#         print(f"AppConfig(env={self.env}, debug={self.debug})")


# # ==========================================================
# # 2️⃣ SINGLETON VIA METACLASS
# # ==========================================================
# """
# Metaclass Singleton:
# - Reusable singleton mechanism for many classes.
# - All classes using this metaclass become singleton.
# """


# class SingletonMeta(ABCMeta):
#     _instances: dict[type, object] = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]


# class Logger(metaclass=SingletonMeta):
#     def __init__(self) -> None:
#         self.logs: list[str] = []

#     def log(self, message: str) -> None:
#         self.logs.append(message)
#         print(f"LOG: {message}")


# # ==========================================================
# # 3️⃣ THREAD-SAFE SINGLETON
# # ==========================================================
# """
# Thread-safe Singleton:
# - Prevents race condition when multiple threads create instance
#   at the same time.
# """


# class DatabaseConnection:
#     _instance: DatabaseConnection | None = None
#     _lock = Lock()

#     def __new__(cls) -> DatabaseConnection:
#         if cls._instance is None:
#             with cls._lock:
#                 if cls._instance is None:
#                     cls._instance = super().__new__(cls)
#                     cls._instance.connected = False
#         return cls._instance

#     def connect(self) -> None:
#         if not self.connected:
#             self.connected = True
#             print("Database connected")


# # ==========================================================
# # 4️⃣ MONOSTATE (BORG) - SINGLE STATE, MANY OBJECTS
# # ==========================================================
# """
# Borg / Monostate:
# - Multiple instances are allowed.
# - But all instances share the same state.
# - Not a strict singleton, but often discussed with singleton.
# """


# class SharedState:
#     _shared_state: dict[str, object] = {}

#     def __init__(self) -> None:
#         self.__dict__ = self._shared_state


# class Cache(SharedState):
#     def __init__(self) -> None:
#         super().__init__()
#         if not hasattr(self, "store"):
#             self.store: dict[str, str] = {}

#     def set(self, key: str, value: str) -> None:
#         self.store[key] = value

#     def get(self, key: str) -> str | None:
#         return self.store.get(key)


# # ==========================================================
# # 5️⃣ OPTIONAL: SINGLETON AS INTERFACE + IMPLEMENTATION
# # ==========================================================
# """
# Sometimes we keep abstraction with ABC and make only concrete class singleton.
# """


# class Notifier(ABC):
#     @abstractmethod
#     def send(self, msg: str) -> None:
#         pass


# class NotificationService(Notifier, metaclass=SingletonMeta):
#     def send(self, msg: str) -> None:
#         print(f"NOTIFY: {msg}")


# # ==========================================================
# # 6️⃣ CLIENT / DEMO
# # ==========================================================

# def _thread_job() -> None:
#     db = DatabaseConnection()
#     print(f"DB instance id in thread: {id(db)}")


# if __name__ == "__main__":
#     print("=== 1) Classic Singleton ===")
#     c1 = AppConfigSingleton()
#     c2 = AppConfigSingleton()
#     c1.env = "prod"
#     c1.show()
#     c2.show()
#     print(f"Same instance? {c1 is c2}")

#     print("\n=== 2) Singleton via Metaclass ===")
#     l1 = Logger()
#     l2 = Logger()
#     l1.log("service started")
#     print(f"Same instance? {l1 is l2}")

#     print("\n=== 3) Thread-safe Singleton ===")
#     t1 = Thread(target=_thread_job)
#     t2 = Thread(target=_thread_job)
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()

#     db1 = DatabaseConnection()
#     db2 = DatabaseConnection()
#     db1.connect()
#     print(f"Same instance? {db1 is db2}")

#     print("\n=== 4) Borg / Monostate ===")
#     cache1 = Cache()
#     cache2 = Cache()
#     cache1.set("token", "abc123")
#     print(f"cache2 token: {cache2.get('token')}")
#     print(f"Same object? {cache1 is cache2}")

#     print("\n=== 5) Singleton Service with Interface ===")
#     n1 = NotificationService()
#     n2 = NotificationService()
#     n1.send("Welcome")
#     print(f"Same instance? {n1 is n2}")
