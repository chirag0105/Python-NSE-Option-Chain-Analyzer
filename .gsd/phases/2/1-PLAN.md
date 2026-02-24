---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Verify Data Streaming & Frontend Parsing

## Objective
The backend's `DataManager` caching natively broadcasts the entire `history` block and live `analytics` payload due to the WebSocket streaming `latest_chains` as its core dump logic in `main.py`. This plan validates that the frontend successfully parses this updated structural payload through WebSockets without breaking the current UI.

## Context
- `backend/main.py` -> `manager.broadcast` logic
- `frontend/app.js` (Lines ~148-161) -> `ws.onmessage` event listener.
- We need to capture and log the `history` and `analytics` arrays safely as they land.

## Tasks

<task type="auto">
  <name>Validate Frontend WebSocket Intake</name>
  <files>
    <file>frontend/app.js</file>
  </files>
  <action>
    Inside `ws.onmessage` in `frontend/app.js`:
    1. During the loop `for (const [symbol, data] of Object.entries(payload.data))`, add a simple `console.log` specifically for debugging that reads:
       `console.log(\`[WebSocket] Incoming "\${symbol}" | History Ticks: \${data.history ? data.history.length : 0} | PCR: \${data.analytics?.pcr}\`);`
    2. Confirm that the dashboard successfully continues tracking `underlyingValue` (LTP) alongside printing this debug message.
  </action>
  <verify>grep -q "History Ticks" frontend/app.js</verify>
  <done>Frontend logic now actively reports the size of the historical time-series buffer and explicit analytics metrics without halting execution rendering.</done>
</task>

## Success Criteria
- [ ] Browser `console.log` successfully reports the `history` length growing over time.
- [ ] WebSocket connections remain stable despite the larger nested object payloads sent every N seconds.
