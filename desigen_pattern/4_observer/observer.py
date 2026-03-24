"""
Observer Design Pattern
=======================

Definition
----------
The Observer pattern defines a one-to-many dependency between objects so that
when one object changes its state, all dependent objects are notified and
updated automatically.

Real-Life Analogy
-----------------
Think of YouTube subscriptions:
- You subscribe to a channel.
- The channel uploads a new video.
- All subscribers get notified automatically.

Core Components
---------------
1. Subject (Publisher)
   - Maintains a list of observers.
   - Provides methods to attach and detach observers.
   - Notifies all observers when its state changes.

2. Observer (Subscriber)
   - Defines the update interface.
   - Receives changes from the subject.

3. Concrete Subject
   - Stores the actual state.
   - Triggers notifications whenever the state changes.

4. Concrete Observer
   - Implements the update behavior.
   - Decides how to react when notified.

Flow
----
Subject -> keeps list of observers
State changes in subject
Subject notifies all observers
Observers react to the new state

When to Use
-----------
- When multiple objects should react automatically to a change in one object.
- In event-driven systems.
- In notification systems.
- In stock price, chat, and live dashboard updates.
- In MVC, where views react to model changes.

Advantages
----------
- Loose coupling between subject and observers.
- Easy to add or remove observers at runtime.
- Supports broadcast-style communication.
- Follows the Open/Closed Principle well.

Disadvantages
-------------
- Too many observers can affect performance.
- Harder to debug because updates happen automatically.
- Can lead to memory leaks if observers are not removed properly.

Observer vs Pub-Sub
-------------------
Observer:
- Subject knows its observers directly.
- Communication is usually in-process and tightly related to object design.

Pub-Sub:
- Publisher and subscriber do not know each other directly.
- A message broker or event bus sits in between.
- Better for distributed and decoupled systems.

Interview One-Liner
-------------------
Use Observer when one object's state change should automatically notify many
dependent objects without tightly coupling their behavior.
"""

from abc import ABC, abstractmethod

#observer interface class
class Observer(ABC):
    @abstractmethod
    def update(self, state):
        pass


#observe interface class
class Subject(ABC):
    @abstractmethod
    def attach(self, observer : Observer):
        pass

    @abstractmethod
    def detach(self, observer : Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


#observe concrete class
class YouToubeChannel(Subject):
    def __init__(self):
        self._observer = []
        self._state = None

    def attach(self, observer : Observer):
       self._observer.append(observer)
 
    
    def detach(self, observer : Observer):
        self._observer.remove(observer)

    def notify(self):
        for observer in self._observer:
            observer.update(self._state)

    def set_state(self,message):
        self._state = message
        self.notify()


#observer concrete calss
class EmailSubscriber(Observer):
    def update(self, state):
        print(f"email subscriber reveived message : {state}")


class MobileSubscriber(Observer):
    def update(self, state):
        print(f"mobile subscriber reveived message : {state}")


if __name__== "__main__":
    channel = YouToubeChannel()

    channel.attach(EmailSubscriber())
    channel.attach(MobileSubscriber())

    channel.set_state(message='observer desigen pattern has been uploaded')
    
        


        
    


    






# class Observer:
#     """Base observer interface."""

#     def update(self, state):
#         raise NotImplementedError("Subclasses must implement update().")


# class Subject:
#     """Maintains observers and notifies them when state changes."""

#     def __init__(self):
#         self._observers = []
#         self._state = None

#     def attach(self, observer):
#         if observer not in self._observers:
#             self._observers.append(observer)

#     def detach(self, observer):
#         if observer in self._observers:
#             self._observers.remove(observer)

#     def notify(self):
#         for observer in self._observers:
#             observer.update(self._state)

#     def set_state(self, state):
#         self._state = state
#         self.notify()


# class EmailSubscriber(Observer):
#     def update(self, state):
#         print(f"Email Subscriber received update: {state}")


# class MobileSubscriber(Observer):
#     def update(self, state):
#         print(f"Mobile Subscriber received update: {state}")


# if __name__ == "__main__":
#     channel = Subject()

#     email_user = EmailSubscriber()
#     mobile_user = MobileSubscriber()

#     channel.attach(email_user)
#     channel.attach(mobile_user)

#     print("Uploading a new video...")
#     channel.set_state("New video uploaded: Observer Pattern in 5 Minutes")
