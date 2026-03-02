"""
Strategy Design Pattern (Python)

Interview prep notes:
- Intent: Define a family of algorithms, encapsulate each one, and make them
  interchangeable. The Strategy lets the algorithm vary independently from
  clients that use it.

- When to use:
  - You have multiple ways to do the same thing (pricing, sorting, routing).
  - You want to avoid large if/elif chains.
  - You want to swap behavior at runtime (A/B tests, feature flags).

- Pros:
  - Open/Closed: add new strategies without modifying existing client logic.
  - Better testability: strategies are small and isolated.

- Cons:
  - More classes/functions.
  - Client must choose a strategy.

Key roles:
- Strategy interface: common method signature.
- Concrete strategies: implementations of the interf ace.
- Context: uses a strategy and delegates work to it.
"""
from __future__ import annotations
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self):
        pass

class UpiPayment(Payment):
    def pay(self):
        print(f"this is upi paynent method")

class CreditCardPayment(Payment):
    def pay(self):
        print(f"this is credit card paynent method")

class DebitCardPayment(Payment):
    def pay(self):
        print(f"this is debit card paynent method")\
        

class PaymentServie:
    def __init__(self, payment : Payment):
        self._payment = payment

    def pay(self):
        self._payment.pay()


if __name__ == "__main__":
    payment_service = [PaymentServie(UpiPayment()),
                       PaymentServie(DebitCardPayment()),
                       PaymentServie(CreditCardPayment())
                    ]
    
    for service in payment_service:
        service.pay()
    
    
    










# from __future__ import annotations

# from abc import ABC, abstractmethod

# # ----------------------------
# # Behavior Interfaces (Strategy)
# # ----------------------------

# class Talkable(ABC):
#     @abstractmethod
#     def talk(self) -> str:
#         pass

# class Walkable(ABC):
#     @abstractmethod
#     def walk(self) -> str:
#         pass

# class Flyable(ABC):
#     @abstractmethod
#     def fly(self) -> str:
#         pass


# # ----------------------------
# # Talk Behaviors
# # ----------------------------
# class NormalTalk(Talkable):
#     def talk(self) -> str:
#         print("Hello, I am a normal talker.")
    
# class NoTalk(Talkable):
#     def talk(self) -> str:
#         print("I cannot talk.")

# # ----------------------------
# # Walk Behaviors
# # ----------------------------
# class NormalWalk(Walkable):
#     def walk(self) -> str:
#         print("I am walking normally.")
    
# class NoWalk(Walkable):
#     def walk(self) -> str:
#         print("I cannot walk.")

# # ----------------------------
# # Fly Behaviors
# # ----------------------------
# class NormalFly(Flyable):
#     def fly(self) -> str:
#         print("I am flying.")
    
# class NoFly(Flyable):
#     def fly(self) -> str:
#         print("I cannot fly.")  


# # ----------------------------
# # Base Robot Class
# # ----------------------------
# class Robot:
#     def __init__(self, talk_behavior: Talkable, walk_behavior: Walkable, fly_behavior: Flyable):
#         self.talk_behavior = talk_behavior
#         self.walk_behavior = walk_behavior
#         self.fly_behavior = fly_behavior

#     def perform_talk(self):
#         self.talk_behavior.talk()

#     def perform_walk(self):
#         self.walk_behavior.walk()

#     def perform_fly(self):
#         self.fly_behavior.fly() 

#     def projection(self):
#         print("I am a robot projection.")


# # ----------------------------
# # Concrete Robot
# # ----------------------------

# class CompanionRobot(Robot):
#     def projection(self) -> None:
#         print("Companion Robot projecting in 3D...")

# # ----------------------------
# # Usage (as shown in diagram)
# # ----------------------------

# if __name__ == "__main__":
#     robot = CompanionRobot(
#         NormalTalk(),
#         NormalWalk(),
#         NoFly(),
#     )

#     robot.perform_talk()
#     robot.perform_walk()
#     robot.perform_fly()
#     robot.projection()










