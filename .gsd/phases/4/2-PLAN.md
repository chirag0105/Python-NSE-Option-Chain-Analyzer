---
phase: 4
plan: 2
wave: 2
---

# Plan 4.2: Frontend — Detail Modal & Card Expand UX

## Objective
Wire up the "expand" interaction: clicking a summary card opens a stylised full-screen detail modal showing the complete 20-strike chain table, with a smooth slide-in animation and a close button.

## Context
- .gsd/DECISIONS.md
- frontend/index.html
- frontend/style.css
- frontend/app.js

## Tasks

<task type="manual">
  <name>Detail Modal HTML & CSS</name>
  <files>
    - frontend/index.html
    - frontend/style.css
  </files>
  <action>
    - Add a `<div id="detail-modal" class="modal hidden">` block to `index.html` with an inner `<div class="modal-content glass-panel detail-panel">`.
    - Inside the detail panel: a `.detail-header` (symbol name + close `✕` button), a `.detail-meta` row (underlying value, expiry, timestamp), and a `<table id="detail-table" class="options-table detail-table">` with appropriate columns.
    - In `style.css` add `.detail-panel` with `max-width: 900px; max-height: 90vh; overflow-y: auto;` and a slide-in animation `@keyframes slideUp { from { transform: translateY(40px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }` applied to the modal-content on show.
    - Add `.detail-atm-row` highlight class — a subtle coloured background marking the ATM strike row.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/index.html'))"</verify>
  <done>Detail modal DOM structure exists and renders correctly with slide-in CSS animation.</done>
</task>

<task type="manual">
  <name>Expand Logic and Live Detail Updates (JS)</name>
  <files>
    - frontend/app.js
  </files>
  <action>
    - In `updateOrBuildCard`, make the card header clickable: add an `onclick="openDetailModal('${symbol}')"` attribute.
    - Write `openDetailModal(symbol)`: fetch `/api/chain/${symbol}`, populate `#detail-table` rows, show the modal.
    - Write `populateDetailTable(data)` building `<tr>` rows for each strike in `data.options_data`. Mark the ATM row (the one where strikPrice is closest to `data.underlyingValue`) with `class="detail-atm-row"`.
    - Write `closeDetailModal()` bound to the `✕` button and a click on the modal backdrop.
    - When the modal is open, also update the detail table from incoming WS messages so numbers stay live — check `if (openSymbol && payload.data[openSymbol])` before re-populating.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/app.js'))"</verify>
  <done>Clicking any card opens the detail modal with all 20 strikes live-updated via WS; closing it returns to the dashboard.</done>
</task>

## Success Criteria
- [ ] Clicking a card opens the detail modal with all 20-strike rows.
- [ ] ATM strike row is visually highlighted.
- [ ] Modal data continues updating while open via WebSocket messages.
- [ ] Close button and backdrop click both hide the modal.
