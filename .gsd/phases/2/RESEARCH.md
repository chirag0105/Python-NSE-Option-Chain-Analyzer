# RESEARCH: Phase 2 - Live Data Streaming (WebSockets)

## Research Focus
- Designing an efficient real-time broadcast system.
- Extracting necessary information from the raw NSE Option Chain API.
- Determining exactly how to pipe new data down to connected clients.

## Findings

**1. WebSocket Architecture in FastAPI**
FastAPI uses Starlette's WebSocket implementation, allowing asynchronous `await websocket.accept()`, `await websocket.send_json(data)`, and connection management. A simple `ConnectionManager` class holding a list of active websocket connections will suffice, giving us a `.broadcast(data)` method.

**2. Data Processor Refinement**
Raw NSE Option Chain responses are hundreds of kilobytes of nested arrays, heavily slowing down WebSockets if sent verbatim. In Phase 1 we cache the raw data in `DataManager.latest_chains`.
Instead of doing this, the `DataManager` should pass the payload to a `DataProcessor` before caching, returning a trimmed dictionary. This trimmed data holds:
- Underlying Value (Current Asset Price)
- Formatted timestamp
- The option chain table (Strike Price, Call OI, Call Chng in OI, Call Volume, Call LTP, Put LTP, Put Volume, Put Chng in OI, Put OI) for a limited range of strikes around the ATM (At-The-Money) to compress size.

**3. Integration into the existing Poller**
In `main.py`, the `background_poll` fetches data and calls `data_manager.update_chain(...)`. Immediately after a successful poll round, we can call `connection_manager.broadcast()`, passing down the transformed caching dictionary. The frontend thus only receives lightweight, fully processed rendering objects.

## Technical Direction
- Build a WebSocket `ConnectionManager` in `backend/websocket_manager.py`.
- Build a `DataProcessor` class in `backend/data_processor.py` wrapping standard Python or Pandas extraction replicating the math previously handled in `NSE_Option_Chain_Analyzer.py`.
- Expose `/api/ws` endpoint in `backend/routers.py`.
- Hook `websocket_manager.broadcast` into the end of the `main.py` poll cycle.
