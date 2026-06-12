---
name: python-async-microservice
description: 'Developing, refactoring, or optimizing Python microservices, asynchronous workers, task queues, or API clients.'
---

# Goal
Produce clean, production-grade Python code utilizing native asynchronous programming paradigms (`asyncio`) paired with strict static type hint compliance.

# Instructions
1. **Explicit Type Hinting:** Enforce comprehensive type gesturing across all function definitions. Use the `typing` module (or built-in collections for Python 3.9+) to define parameters, optional variables (`Optional[T]`), and expected return types.
2. **Non-Blocking I/O operations:** When dealing with network I/O, database queries, or downstream service communications, consistently employ `async`/`await` primitives alongside fully asynchronous client libraries (such as `httpx` or `aiogrpc`).
3. **Robust Resource Lifecycle:** Utilize asynchronous context managers (`async with`) for handling network connections, file structures, or client sessions to guarantee proper resource release upon execution termination.
4. **Resilient Data Parsing:** Employ `Pydantic` models or native `dataclasses` to parse and structurally validate incoming external request payloads before routing them into your execution layer.

# Constraints
- Do not make synchronous blocking calls (like `time.sleep()` or standard `requests`) inside `async def` scopes; always substitute with their non-blocking counterparts (`asyncio.sleep()`).
- Avoid global mutable states across independent worker threads or coroutines.