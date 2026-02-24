---
phase: 2
plan: 2
wave: 2
---

# Plan 2.2: Data Processor and Broadcast Integration

## Objective
Extract key NSE Option Chain fields safely out of the large raw JSON into a minimal dashboard dict format and dispatch the processed states across the open WebSockets.

## Context
- .gsd/ROADMAP.md
- .gsd/phases/2/RESEARCH.md
- backend/main.py

## Tasks

<task type="auto">
  <name>Build DataProcessor Utility</name>
  <files>
    - backend/data_processor.py
  </files>
  <action>
    - Create a class `DataProcessor` with a classmethod `process_chain(raw_payload: dict, limit_strikes: int = 10)`.
    - It should read `raw_payload['records']['data']` and find the current `underlyingValue` (the asset price), reading the closest expiry string.
    - Sort the list of option chains by strike price. Find the ATM (At-The-Money) index using `underlyingValue`, then slice exactly `limit_strikes/2` rows above it and `limit_strikes/2` rows below it.
    - Create a dictionary holding `"symbol"`, `"timestamp"`, `"underlyingValue"`, and `"options_data": []` representing the filtered rows mapping minimal fields (Call OI, Call LTP, Call Vol, Strike, Put LTP, Put OI, Put Vol).
    - Return this clean structure.
  </action>
  <verify>python -c "import pandas"</verify>
  <done>DataProcessor.process_chain strips useless JSON data and leaves only a small subset of meaningful At-The-Money strike prices.</done>
</task>

<task type="auto">
  <name>Integrate Poller with Broadcaster</name>
  <files>
    - backend/main.py
    - backend/data_processor.py
    - backend/websocket_manager.py
    - backend/data_manager.py
  </files>
  <action>
    - Import `DataProcessor` and `manager` inside `main.py`.
    - Update the `background_poll` looping block: After `data = await nse_client.fetch_option_chain`, pass it through `processed = DataProcessor.process_chain(data)`.
    - Modify `data_manager.update_chain(...)` to cache the `processed` data dictionary instead of raw JSON.
    - Right before the loop yields its final `await asyncio.sleep(interval)` block, do `await manager.broadcast({"type": "update", "data": data_manager.latest_chains})` to ship the newly cached dict down the wire.
  </action>
  <verify>python -c "import fastapi"</verify>
  <done>Upon loop completion, all active websockets receive the processed dictionary block natively.</done>
</task>

## Success Criteria
- [ ] Raw JSON from NSE API is reduced in size successfully.
- [ ] Active websocket connections accurately receive pushed updates containing fresh data at loop closures.
- [ ] DataManager explicitly only stores minimal objects freeing RAM.
