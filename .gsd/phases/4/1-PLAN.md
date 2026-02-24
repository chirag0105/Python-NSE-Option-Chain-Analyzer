---
phase: 4
plan: 1
wave: 1
---

# Plan 4.1: Backend — Deep Chain REST Endpoint

## Objective
Add a `/api/chain/{symbol}` GET endpoint that returns the full 20-strike processed chain snapshot on demand, so the detail modal can fetch fresh data independent of the WS broadcast cycle.

## Context
- .gsd/DECISIONS.md
- backend/routers.py
- backend/data_processor.py
- backend/data_manager.py

## Tasks

<task type="auto">
  <name>Add /api/chain/{symbol} endpoint</name>
  <files>
    - backend/routers.py
  </files>
  <action>
    - Add `@api_router.get("/chain/{symbol}")` to `routers.py`.
    - The handler should first check `data_manager.latest_chains.get(symbol)`. If data exists in cache, return it immediately.
    - If the symbol is not yet cached (first open), return a 404 with a meaningful message like `{"error": "Symbol not yet available. Try again shortly."}`.
    - Add `from fastapi import HTTPException` to handle the 404 cleanly.
  </action>
  <verify>python -c "from fastapi import HTTPException"</verify>
  <done>GET /api/chain/NIFTY returns the full 20-strike option chain payload from in-memory cache.</done>
</task>

## Success Criteria
- [ ] `/api/chain/{symbol}` returns cached chain data as JSON, or a 404 if not cached yet.
