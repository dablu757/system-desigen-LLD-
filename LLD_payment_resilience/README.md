# Payment API Spike Handling - Design Document

## Problem Statement

Your app depends on a third-party payment API that cannot be modified.
During request spikes, directly forwarding all requests can:
- overload the provider
- hit rate limits
- increase timeouts/failures

## Goal

Protect the third-party payment API while maximizing successful payments and keeping user experience predictable.

## Proposed Solution (High Level)

Use an **asynchronous buffer + controlled workers** pattern:

1. Accept incoming payment requests quickly.
2. Store each request in a durable queue.
3. Process queue with worker pool at a controlled rate.
4. Add resilience patterns around provider calls.

This decouples traffic spikes from provider capacity.

## Architecture

- API Layer
  - Validates request
  - Creates idempotency key
  - Enqueues payment job
  - Returns `202 Accepted` + tracking id
- Queue
  - Durable message queue (Redis Streams/RabbitMQ/SQS/Kafka)
  - Absorbs spikes
- Worker Service
  - Pulls jobs from queue
  - Calls provider through rate limiter and circuit breaker
  - Writes result to payment status store
- Status Store
  - `PENDING`, `PROCESSING`, `SUCCESS`, `FAILED`, `RETRYING`, `DEAD_LETTER`
- DLQ (Dead Letter Queue)
  - Stores exhausted retries for manual/replay handling

## Core Patterns

## 1) Rate Limiting (mandatory)

Use token-bucket or leaky-bucket in workers so provider call volume stays under allowed RPS.

Example:
- Provider limit: 100 RPS
- Configure worker limiter: 80-90 RPS for safety margin

## 2) Retry with Exponential Backoff + Jitter

Retry only transient failures:
- 429
- 5xx
- network timeouts

Do not retry permanent failures:
- invalid card
- validation error

Backoff example:
- 1s, 2s, 4s, 8s (+random jitter)
- max attempts = 5

## 3) Circuit Breaker

If provider keeps failing:
- open circuit temporarily
- stop hammering provider
- fail fast or defer requests
- move to half-open later for probe requests

## 4) Idempotency

Use unique key per payment intent/order to prevent duplicate charges during retries and network uncertainty.

## 5) Backpressure & Admission Control

If queue depth is too high:
- degrade gracefully
- reject new requests with clear message
- or enqueue with delayed processing SLA

## 6) Priority Queues (optional)

Separate queues for:
- premium users
- normal users
- retries

This prevents starvation and improves fairness.

## Request Flow

1. Client sends payment request.
2. API validates payload and idempotency key.
3. API stores payment record as `PENDING`.
4. API enqueues job and returns tracking id.
5. Worker takes job, applies rate-limit + circuit breaker.
6. Worker calls provider.
7. On success -> `SUCCESS`.
8. On transient failure -> `RETRYING` (requeue with delay).
9. On retry exhaustion -> `DEAD_LETTER`.

## Data Model (Minimal)

`payment_requests`
- `payment_id` (PK)
- `order_id`
- `idempotency_key` (unique)
- `amount`, `currency`
- `status`
- `attempt_count`
- `next_retry_at`
- `provider_txn_id`
- `error_code`, `error_message`
- `created_at`, `updated_at`

## API Contracts (Suggested)

- `POST /payments`
  - returns `202 Accepted`
  - body: `{payment_id, status="PENDING"}`
- `GET /payments/{payment_id}`
  - returns latest status

## Operational Metrics

Track and alert on:
- queue depth
- processing latency (enqueue->done)
- provider success rate
- 429/5xx rate
- retry count and DLQ size
- circuit breaker state

## Capacity Guidelines

- Queue retention should cover peak burst duration.
- Worker autoscaling should depend on queue lag and provider headroom.
- Rate limiter must remain below provider published or observed safe throughput.

## Why This Works

- Spikes are absorbed by queue instead of hitting provider instantly.
- Worker throughput is controlled and stable.
- Retries recover transient failures safely.
- Circuit breaker prevents cascading outages.
- Idempotency prevents double charging.

## Trade-offs

- Payments become eventually consistent (not instant under heavy spike).
- More moving parts (queue, workers, monitoring).
- Requires robust status tracking for client visibility.

## Rollout Plan

1. Add idempotency + status table.
2. Introduce async queue behind existing API.
3. Enable worker rate limiter.
4. Add retry policy + DLQ.
5. Add circuit breaker.
6. Add dashboards and alerting.
7. Tune limits with real traffic.
