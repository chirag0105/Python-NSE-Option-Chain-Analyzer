---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: WebSocket Connection Manager

## Objective
Implement native WebSockets in FastAPI to manage active connections and broadcast updates down to the frontend dashboard.

## Context
- .gsd/ROADMAP.md
- .gsd/phases/2/RESEARCH.md
- backend/routers.py

## Tasks

<task type="auto">
  <name>Create WebSocketManager Class</name>
  <files>
    - backend/websocket_manager.py
  </files>
  <action>
    - Define a `ConnectionManager` class.
    - Inside, hold a list `self.active_connections: List[WebSocket] = []`.
    - Implement `async def connect(self, websocket: WebSocket): await websocket.accept(); self.active_connections.append(websocket)`.
    - Implement `def disconnect(self, websocket: WebSocket): self.active_connections.remove(websocket)`.
    - Implement `async def broadcast(self, message: dict): [await connection.send_json(message) for connection in self.active_connections]`.
    - Instantiate a singleton `manager = ConnectionManager()`.
  </action>
  <verify>python -c "from fastapi import WebSocket"</verify>
  <done>ConnectionManager is implemented with full capability to maintain states and broadcast dictionaries.</done>
</task>

<task type="auto">
  <name>Expose /api/ws Endpoint</name>
  <files>
    - backend/routers.py
    - backend/websocket_manager.py
    - backend/data_manager.py
  </files>
  <action>
    - In `routers.py`, import `WebSocket`, `WebSocketDisconnect` from fastapi.
    - Import the singleton `manager` from `websocket_manager.py`.
    - Create a `@api_router.websocket("/ws")` router catching WebSocket requests.
    - Initialize the connection via `await manager.connect(websocket)`.
    - Automatically send the current state of `data_manager.latest_chains` down to the client immediately upon connection so they don't have to wait for the next polling interval.
    - Maintain an infinite loop `while True: await websocket.receive_text()` to keep the connection open, with a standard `except WebSocketDisconnect` breaking the loop and calling `manager.disconnect(websocket)`.
  </action>
  <verify>python -c "import fastapi"</verify>
  <done>The `/api/ws` endpoint successfully allows clients to connect and pushes immediate cache state.</done>
</task>

## Success Criteria
- [ ] Websocket manager holds a list of active open socket descriptors.
- [ ] Connectors are correctly dropped upon disconnection gracefully.
- [ ] Clients receive the initial cached array upon the first connect.
