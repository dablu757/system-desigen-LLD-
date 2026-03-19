# Observer Pattern in Python

This module demonstrates the Observer design pattern using a YouTube channel
subscription example.

Source file: `desigen_pattern/observer/observer.py`

## Intent

Define a one-to-many dependency between objects so that when one object changes
state, all its dependents are notified and updated automatically.

## Real-Life Analogy

Think of YouTube subscriptions:

- A user subscribes to a channel.
- The channel uploads a new video.
- All subscribers get notified automatically.

## Participants

### 1) Observer

Defines the contract for all subscribers.

In this code:
- `Observer`

It exposes:
- `update(message)`

### 2) Subject

Defines the contract for the publisher.

Responsibilities:
- Attach observers
- Detach observers
- Notify all observers

### 3) Concrete Subject

The actual publisher whose state changes.

In this code:
- `YouTubeChannel`

It:
- Stores the list of observers
- Stores the latest uploaded video
- Notifies all subscribers when a new video is uploaded

### 4) Concrete Observers

Actual subscribers that react to updates.

In this code:
- `EmailSubscriber`
- `MobileSubscriber`

## Flow

1. Observers subscribe to the subject using `attach()`.
2. Subject state changes, for example a new video is uploaded.
3. Subject calls `notify()`.
4. Each observer receives the update through `update()`.

## When to Use

- When many objects need automatic updates from one object
- Notification systems
- Event listeners
- GUI frameworks
- Stock price or chat app updates
- MVC systems where views react to model changes

## Advantages

- Loose coupling between publisher and subscribers
- Easy to add new observers without changing subject logic
- Supports broadcast communication
- Good for event-driven systems

## Disadvantages

- Too many observers can reduce performance
- Debugging can become harder because updates are automatic
- Observers must be removed carefully to avoid memory leaks

## Observer vs Pub-Sub

- **Observer**:
  - Subject knows observers directly
  - Usually used inside the same application or object graph

- **Pub-Sub**:
  - Publisher and subscriber do not know each other directly
  - Communication happens through a broker or event bus

In short:
- Observer = direct relationship
- Pub-Sub = broker-based communication

## Interview Tip

If asked whether `Subject` and `Observer` should both be interfaces:

- `Observer` is usually made abstract because every observer must implement
  `update()`.
- `Subject` can also be abstract to enforce `attach()`, `detach()`, and
  `notify()`.
- In simple interview code, making `Observer` abstract and keeping `Subject`
  concrete is also acceptable.

## Example Output

```text
Uploading a new video...
Email Subscriber received update: Observer Pattern Explained
Mobile Subscriber received update: Observer Pattern Explained
```

## Summary

The Observer pattern is best when one object's change should automatically
notify multiple dependent objects without tightly coupling them together.
