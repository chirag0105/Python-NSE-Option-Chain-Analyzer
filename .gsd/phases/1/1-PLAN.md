---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Initialize Backend Structure and Configuration

## Objective
Establish the FastAPI application foundation and a configuration manager to store JSON settings (similar to the old `.ini` mechanism).

## Context
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- .gsd/phases/1/RESEARCH.md

## Tasks

<task type="auto">
  <name>Initialize FastAPI and requirements</name>
  <files>
    - backend/main.py
    - requirements.txt
  </files>
  <action>
    - Update `requirements.txt` to include `fastapi`, `uvicorn`, and `httpx`.
    - Create `backend/main.py` initializing a basic FastAPI application.
    - Add a simple `/api/health` GET endpoint returning `{"status": "ok"}`.
  </action>
  <verify>python -c "import fastapi"</verify>
  <done>FastAPI runs, and `/api/health` indicates ok.</done>
</task>

<task type="auto">
  <name>Configuration Manager</name>
  <files>
    - backend/config_manager.py
    - backend/models.py
  </files>
  <action>
    - Define a backend Pydantic model (`AppConfig`) storing an array of active scripts (e.g. `[{"symbol": "NIFTY", "type": "index"}]`) and a string `refresh_interval`.
    - Implement `ConfigManager` in `config_manager.py` that reads and writes this Pydantic model to a `config.json` file on disk asynchronously.
    - If `config.json` doesn't exist, seed it with a default configuration block (e.g. NIFTY and 30s interval).
  </action>
  <verify>python -c "import pydantic"</verify>
  <done>ConfigManager successfully saves and loads dictionary representations of user configurations to disk.</done>
</task>

## Success Criteria
- [ ] FastAPI structure exists and is healthy.
- [ ] Configuration manager correctly models and stores data in a `config.json` file.
