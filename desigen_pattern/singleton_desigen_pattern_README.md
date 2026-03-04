# Singleton Design Pattern in Python

This module demonstrates multiple singleton-style approaches in Python.

Source file: `desigen_pattern/singleton_desigen_pattern.py`

## What is Singleton?

Singleton is a creational design pattern that ensures a class has only one instance and provides a global access point to that instance.

Typical use cases:
- Application configuration
- Logger service
- Database connection manager
- Shared in-memory cache

## Implementations Covered

## 1) Classic Singleton (`__new__`)

Class: `AppConfigSingleton`

### Idea
Override `__new__` and keep a class-level `_instance` reference.

### Flow
1. First object creation sets `_instance`.
2. Next calls return the same stored object.
3. Any state changes are visible from all references.

### Pros
- Simple and explicit.
- Easy to understand.

### Cons
- Not thread-safe by default.

## 2) Singleton via Metaclass

Metaclass: `SingletonMeta`  
Class example: `Logger`

### Idea
Put singleton logic in metaclass `__call__`, so any class using this metaclass becomes singleton automatically.

### Flow
1. `SingletonMeta.__call__` checks if instance exists in `_instances`.
2. If not, create and store it.
3. Return stored instance on every call.

### Pros
- Reusable across many classes.
- Centralized singleton behavior.

### Cons
- Slightly advanced Python concept for beginners.

## 3) Thread-safe Singleton

Class: `DatabaseConnection`

### Idea
Use `Lock` + double-checked locking in `__new__`.

### Why
In multi-threaded apps, two threads may create separate objects at the same time without synchronization.

### Flow
1. Check `_instance` outside lock (fast path).
2. Acquire lock.
3. Re-check `_instance` inside lock.
4. Create only once.

### Pros
- Safe in concurrent environments.

### Cons
- Slightly more complex than classic singleton.

## 4) Borg / Monostate (Singleton-like)

Base class: `SharedState`  
Concrete example: `Cache`

### Idea
Not single object identity. Instead, all instances share the same internal state dictionary.

### Behavior
- `cache1 is cache2` -> `False`
- But state written from one is visible in the other.

### Use case
When shared state is needed but strict singleton identity is not required.

## 5) Singleton with Abstraction (ABC + Singleton)

Interface: `Notifier`  
Concrete singleton: `NotificationService`

### Idea
Keep interface-driven design while preserving singleton behavior in concrete implementation.

In this file, `SingletonMeta` inherits from `ABCMeta`, so classes can be both abstract/interface-based and singleton-enabled.

## How to Run

From project root:

```bash
python3 desigen_pattern/singleton_desigen_pattern.py
```

## Expected Output (Sample)

```text
=== 1) Classic Singleton ===
AppConfig(env=prod, debug=True)
AppConfig(env=prod, debug=True)
Same instance? True

=== 2) Singleton via Metaclass ===
LOG: service started
Same instance? True

=== 3) Thread-safe Singleton ===
DB instance id in thread: <same id>
DB instance id in thread: <same id>
Database connected
Same instance? True

=== 4) Borg / Monostate ===
cache2 token: abc123
Same object? False

=== 5) Singleton Service with Interface ===
NOTIFY: Welcome
Same instance? True
```

## Comparison Table

| Approach | Single Object Identity | Thread-safe | Reusable | Complexity |
|---|---|---|---|---|
| Classic (`__new__`) | Yes | No | Medium | Low |
| Metaclass | Yes | No (unless lock added) | High | Medium |
| Thread-safe (`Lock`) | Yes | Yes | Medium | Medium |
| Borg/Monostate | No (shared state only) | Depends | Medium | Medium |

## Best Practices

- Use singleton only for true shared resources.
- Avoid overusing global mutable state.
- For multi-threading, prefer a thread-safe implementation.
- Keep dependencies injectable in large systems to maintain testability.

## File Summary

- `AppConfigSingleton`: classic singleton config object
- `SingletonMeta`: reusable singleton metaclass
- `Logger`: metaclass singleton demo
- `DatabaseConnection`: thread-safe singleton demo
- `SharedState`/`Cache`: Borg pattern demo
- `Notifier`/`NotificationService`: interface + singleton demo
