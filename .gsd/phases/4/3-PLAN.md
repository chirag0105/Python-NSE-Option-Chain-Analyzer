---
phase: 4
plan: 3
wave: 3
---

# Plan 4.3: UX Polish — Connection Badge, Loading States & Mobile

## Objective
Ship three polish items: (1) a live WebSocket connection status badge in the header, (2) skeleton loading states on cards before data arrives, and (3) a mobile-responsive CSS pass.

## Context
- .gsd/DECISIONS.md
- frontend/style.css
- frontend/app.js
- frontend/index.html

## Tasks

<task type="manual">
  <name>Connection Status Badge & Card Loading State</name>
  <files>
    - frontend/index.html
    - frontend/style.css
    - frontend/app.js
  </files>
  <action>
    - Add `<span id="ws-status" class="ws-badge disconnected">● Disconnected</span>` to the header in `index.html`.
    - In `style.css` define `.ws-badge`, `.ws-badge.live { color: var(--positive); }`, `.ws-badge.disconnected { color: var(--negative); }` with a `@keyframes pulse` glow on `.live`.
    - In `app.js` `connectWebSocket()`: set `document.getElementById('ws-status').className = 'ws-badge live'; document.getElementById('ws-status').textContent = '● Live';` on `ws.onopen`, and set back to `disconnected` on `ws.onclose`.
    - Add a skeleton loading state: when `updateOrBuildCard` creates a card for the first time, insert a `.skeleton` placeholder shimmer div inside the card while the first real data arrives (replace on first WS update).
    - In `style.css` add `.skeleton { background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%); animation: shimmer 1.5s infinite; border-radius: 4px; }` and `@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }`.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/app.js'))"</verify>
  <done>Header shows a pulsing green ● Live badge when WS is connected, skeleton shimmer on card first-load.</done>
</task>

<task type="manual">
  <name>Mobile Responsiveness CSS Pass</name>
  <files>
    - frontend/style.css
  </files>
  <action>
    - Add `@media (max-width: 768px)` block to `style.css` with:
      - `header { padding: 1rem 1.5rem; }` 
      - `.dashboard-grid { grid-template-columns: 1fr; padding: 1.5rem 1rem; gap: 1rem; }`
      - `.modal-content { width: 95%; max-height: 85vh; }`
      - `.options-table { font-size: 0.8rem; }`
      - `h1 { font-size: 1.2rem; }` and `.underlying-value { font-size: 1.1rem; }`
    - Also add `@media (max-width: 480px)` for smallest screens: hide `Call OI` and `Put OI` columns using CSS class toggling to keep the table readable.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/style.css'))"</verify>
  <done>Dashboard renders cleanly on mobile with single-column stacked cards and compact table layout.</done>
</task>

## Success Criteria
- [ ] WS status badge shows correctly on connect/disconnect.
- [ ] Card shimmer skeleton visible on first load before data arrives.
- [ ] Dashboard is usable on screens down to 375px wide.
