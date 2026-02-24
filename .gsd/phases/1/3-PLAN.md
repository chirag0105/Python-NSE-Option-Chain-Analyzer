---
phase: 1
plan: 3
wave: 2
---

# Plan 1.3: Background Polling Loop and Refined Data Manager

## Objective
Establish the polling infrastructure in FastAPI using the native `lifespan` context manager and implement a `DataManager` responsible for calling the `NSEClient` to cache standard option chain rows for the dashboard.

## Context
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/phases/1/RESEARCH.md

## Tasks

<task type="auto">
  <name>Background Polling Loop via Lifespan</name>
  <files>
    - backend/main.py
    - backend/data_manager.py
    - backend/config_manager.py
  </files>
  <action>
    - Ensure `DataManager` class exists to hold `.latest_chains = {}` in-memory.
    - Inside `main.py`, define a `lifespan` context manager that initializes `NSEClient` cookies, then triggers an `asyncio.create_task` looping infinitely.
    - Inside the loop, read the requested arrays of arrays inside `ConfigManager`, iterate through each tracked symbol, use `NSEClient` to fetch it, and update `DataManager.latest_chains[symbol]`.
    - Apply `asyncio.sleep` to wait during intervals natively (e.g. 30 seconds default), with a retry catch fallback block inside the loop to avoid silent crashes on timeouts / 401s.
  </action>
  <verify>python -c "import asyncio"</verify>
  <done>Continuous polling correctly caches in memory automatically upon application launch without stalling the web workers.</done>
</task>

<task type="auto">
  <name>Expose REST API configurations</name>
  <files>
    - backend/main.py
    - backend/routers.py
  </files>
  <action>
    - Move endpoints into a dedicated `/api/` router (`routers.py`).
    - Create a GET `/api/config` that returns the parsed `config.json`.
    - Create a POST `/api/config` that accepts a new array of symbols and an interval, saves them to disk using the manager, and modifies the running loop state safely.
  </action>
  <verify>python -c "import fastapi"</verify>
  <done>Frontend can safely manipulate the backend interval / selected symbols via standard REST calls.</done>
</task>

## Success Criteria
- [ ] Application continuously polls the NSE database without crashing natively.
- [ ] User frontend changes are persisted using POST REST hooks successfully interacting with the configuration manager.
