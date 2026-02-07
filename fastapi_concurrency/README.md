# FastAPI Deployment Stack
This repository explains the role and interaction of **FastAPI**, **Uvicorn**, **Gunicorn**, and **httpx** in a modern Python backend system.

---

## 1. FastAPI

**FastAPI** is a modern, high-performance Python web framework used to build APIs.

### Key Features
- High performance (built on Starlette & Pydantic)
- Native `async/await` support
- Automatic API documentation (Swagger UI & ReDoc)
- Request/response validation using type hints
- Ideal for microservices and REST APIs

### Role in the system
FastAPI defines:
- API routes
- Request/response schemas
- Business logic

---

## 2. Uvicorn

**Uvicorn** is an **ASGI server** used to run FastAPI applications.

### Why Uvicorn?
- Supports asynchronous programming
- Handles HTTP requests, WebSockets, background tasks
- Lightweight and very fast

### Common usage
- Local development
- Simple deployments

```bash
uvicorn main:app --reload


Role in the system
----------------------

Uvicorn:
    Listens for incoming requests
    Passes requests to FastAPI
    Returns responses back to the client
----------------------

3. Gunicorn
    Gunicorn is a production-grade process manager.

Why Gunicorn?
    Runs multiple worker processes
    Improves CPU utilization
    Handles worker crashes and restarts
    Designed for production environments
----------------------

FastAPI + Gunicorn
----------------------
    FastAPI is ASGI-based, while Gunicorn is WSGI-based by default.
    To make them work together, Gunicorn uses Uvicorn workers.
----------------------

command to start combilne (guvicorn with uvicorn))
    gunicorn main:app -k uvicorn.workers.UvicornWorker


Role in the system

Gunicorn:
    Manages multiple Uvicorn worker processes
    Improves scalability and reliability in production

----------------------
4. httpx
    httpx is an HTTP client library used to make API calls.

Why httpx instead of requests?

    Supports both sync and async requests
    Non-blocking (perfect for FastAPI)
    Ideal for microservice communication

Example (Async)
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")

Role in the system
- httpx is used when:
    -> Calling external APIs
    -> Communicating between microservices
    -> Fetching data asynchronously inside FastAPI routes
----------------------

##Overall Architecture Flow


        Client
         ↓
Gunicorn (Process Manager)
        ↓
Uvicorn Worker (ASGI Server)
        ↓
FastAPI Application
         ↓
httpx → External Services / APIs

----------------------

# Development vs Production
**Development**
FastAPI + Uvicorn
    Easy debugging
    Auto reload

Production
    Gunicorn + Uvicorn workers
    Multiple processes
    Better performance and fault tolerance

----------------------
Interview One-Liner

    FastAPI is the web framework, Uvicorn is the ASGI server that runs it, Gunicorn manages multiple Uvicorn workers in production, and httpx is used for async HTTP calls to external services.


Q: Can FastAPI run without Uvicorn?
    No. FastAPI needs an ASGI server like Uvicorn or Hypercorn to run.

Q: Why not use Gunicorn alone?
    Gunicorn is WSGI-based by default and does not support async without ASGI workers.

Q: Why is httpx preferred in FastAPI?
    Because it supports async requests and avoids blocking the event loop.

