---
phase: 3
plan: 2
wave: 1
---

# Plan 3.2: Implementing the Historical Data Chart Table

## Objective
Convert the stored chronological `analytics` points arrays inside the new websocket `data.history` into a visual time-series table that updates directly inside the frontend's expanded chain view to fully match the GUI.

## Context
- `frontend/index.html` - Detail Modal body.
- `frontend/app.js` - `updateDetailModalLive` logic loop.

## Tasks

<task type="auto">
  <name>Build the Historical Table View Skeleton</name>
  <files>
    <file>frontend/index.html</file>
  </files>
  <action>
    Add a new `<div class="history-container">` wrapping a newly created `<table>` block inside the nested Detail Modal structure (likely above the raw options-chain table, identical to how the original Tkinter app placed the streaming Log layout first, then the Option Parameters secondly).
    The Headers of this table must track: `Time, Value, Call Sum, Put Sum, Difference, Call Boundary, Put Boundary, Call ITM, Put ITM`.
    Create a `<tbody id="history-table-body">` to hook into via JS.
  </action>
  <verify>grep -q "history-table-body" frontend/index.html</verify>
  <done>History log layout exists dynamically inside the detail-modal.</done>
</task>

<task type="auto">
  <name>Populate Time-Series Log and Coloring</name>
  <files>
    <file>frontend/app.js</file>
  </files>
  <action>
    Inside `updateDetailModalLive`, map the `data.history` array iteratively to paint rows in the `history-table-body`.
    1. Parse through the ticks via a `.forEach`
    2. Format row components tracking the previous tick vs new tick recursively, just like the Python GUI (Lines ~1300-1380).
       - Ex: if new `underlyingValue` is `> old_underlyingValue`, color the value cell `background: #00e676 (green)`, else `#e53935 (red)`.
       - Similarly apply the Green/Red cell shading conditionally on `Call Sum`, `Put Sum`, `Difference`, `Boundaries`, `ITMs` comparing `[Tick N]` vs `[Tick N-1]` if it increased/decreased just like Tkinter did visually in the screenshot.
    3. Fill the table cleanly with the corresponding values tracking the full session session.
  </action>
  <verify>grep -q "history-table-body" frontend/app.js</verify>
  <done>Frontend logic now renders the full dynamic log layout iterating over the historical data array and correctly color blocks increases vs decreases cell-by-cell.</done>
</task>

## Success Criteria
- [ ] Visual history table identically mirrors the running background polling output shown in the top half of the original application GUI screenshot.
- [ ] Users can track momentum shifts and PCR differences through clearly colored cell indicators dynamically mapping their underlying values.
