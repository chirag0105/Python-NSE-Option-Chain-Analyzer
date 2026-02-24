# RESEARCH: Phase 1 - Foundation (Backend)

## Research Focus
- Designing a modern FastAPI backend to replace a monolithic Tkinter Python app.
- Determining exactly how to poll the NSE Option Chain APIs without getting 401s / blocks.
- Establishing the configuration serialization format.

## Findings

**1. FastAPI Framework**
FastAPI naturally handles `asyncio` loops via the new `lifespan` context manager mechanism (or deprecated `on_event("startup")`). Within the lifespan context, we can invoke an `asyncio.create_task` to run a continuous `while True` loop that polls data using the intervals configured by the user, then cleans up upon shutdown.

**2. Session Management for NSE APIs**
Historical evidence from early `NSE_Option_Chain_Analyzer.py` shows constant adjustments to requests: 
- The NSE website uses extensive anti-scraping capabilities. You MUST request the homepage (like `https://www.nseindia.com`) to generate and cache necessary session cookies. 
- You MUST provide mimicking `User-Agent`, `Accept-Language`, and `Accept-Encoding` headers.
- Since we are retrieving JSON, the application must use a library capable of handling asynchronous requests using HTTP/2, ideally `httpx` and `asyncio.sleep()`.
- Data is returned in Brotli `br` encoding, which `httpx` supports natively via the `brotli` package already in requirements.

**3. Configuration (JSON Storage)**
Storing state variables (like selected option chains and intervals) in a JSON file (`config.json`) works well since it's strictly a single-server deployment. JSON is readable, lightweight, and can be completely rewritten during a user's dashboard interaction. 

## Technical Direction
- Extract the core endpoint URLs (`/api/option-chain-indices` and `/api/option-chain-equities`) into an `httpx.AsyncClient` wrapper class.
- The wrapper class will manage a session property, rotating/fetching homepage cookies every few minutes or whenever a request fails.
- The `lifespan` function in `main.py` will start the background polling method.
- Establish initial `/api/config`, `/api/symbols`, and `/api/health` REST endpoints to lay the foundation for the frontend.
