---
phase: 3
plan: 2
wave: 2
---

# Plan 3.2: Configuration State & WebSockets (Vanilla JS)

## Objective
Implement LocalStorage synchronization to retain chosen symbols and build a Vanilla JS WebSocket client mapping incoming streaming data into HTML cards.

## Context
- .gsd/ROADMAP.md
- .gsd/phases/3/RESEARCH.md
- frontend/index.html
- backend/routers.py

## Tasks

<task type="manual">
  <name>State Setup and LocalStorage Manager</name>
  <files>
    - frontend/app.js
  </files>
  <action>
    - Build an initialization function `document.addEventListener("DOMContentLoaded", init)`.
    - `init()` reads `localStorage.getItem("tracked_scripts")`.
    - If `null` or `[]`, display the setup modal via `document.getElementById('setup-modal').classList.remove('hidden')`.
    - Fetch from `/api/symbols`, populating checkboxes in the modal for available Index or Equity tracking.
    - Submit button creates a JSON `[{"symbol": "NIFTY", "type": "index"}]`, saves to `localStorage`, and runs `fetch('/api/config', {method: 'POST'...})`, then hides modal and connects WebSocket.
    - If localStorage data exists, immediately POST and connect without showing the modal.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/app.js'))"</verify>
  <done>Clients correctly bootstrap their settings persistently on reload without bugging the backend config state constantly.</done>
</task>

<task type="manual">
  <name>WebSocket Broadcast Parsing & UI Reactivity</name>
  <files>
    - frontend/app.js
  </files>
  <action>
    - Inside `app.js`, create a constant `ws = new WebSocket("ws://" + window.location.host + "/api/ws")`.
    - Inside `ws.onmessage = function(event)`, parse the incoming JSON payload which matches the `data_manager.latest_chains` dictionary structure.
    - Write a function `updateOrBuildCard(symbol, payload)` checking if `document.getElementById('card-' + symbol)` exists.
    - If not, `.createElement('div')`, add premium glassmorphism `.card` classes, and `.appendChild()` it to `document.getElementById('dashboard-container')`.
    - Parse the payload: Extract `underlyingValue` into a vibrant `.price` span (green for up, red down relative tracking if desired, simple white for now). Output the top 5 `options_data` strikes.
    - Implement a smooth `class.add('flash')` animation natively handling updates for real-time visual polling triggers so it's visibly apparent numbers changed.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/app.js'))"</verify>
  <done>Frontend reacts dynamically to WebSocket messages gracefully inserting Vanilla HTML string replacements across target specific Node IDs efficiently.</done>
</task>

## Success Criteria
- [ ] Local storage holds and restores dashboard environments upon browser refreshes.
- [ ] WebSocket streaming correctly transforms the page DOM asynchronously without refreshing.
- [ ] Visual indicator animations (CSS flashing) successfully fire upon incoming data loops.
