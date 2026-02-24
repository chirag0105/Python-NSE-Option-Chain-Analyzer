---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: Expanding Detail View with Analytics

## Objective
Update the `detail-modal` logic in the web dashboard so that instead of just showing a blown up version of the basic table, it also tracks the history arrays and visualizes the bottom half analytical grid (Upper Boundaries, PCR, Bearish/Bullish labels, ITM checks, etc), exactly like the screenshot provided of the old Tkinter GUI layout.

## Context
- `frontend/index.html` - Specifically the `<div id="detail-modal">` template block. This structure currently only houses the expanded raw table view. It needs placeholders for the metrics indicators.
- `frontend/app.js` - `updateDetailModalLive` logic where we can inject the static elements, and process `data.history` into a new table log.

## Tasks

<task type="auto">
  <name>Draft Analytics UI in Detail Template</name>
  <files>
    <file>frontend/index.html</file>
  </files>
  <action>
    Find `<div class="modal-body">` in `index.html` under `detail-modal`.
    Below the existing `options-table detail-table`, insert the equivalent bottom grids that appear in theTkinter app:
    
    1. A section that explicitly splits Open Interest Boundaries and Exits:
       - Upper Boundary Section
       - Lower Boundary Section
       - "Open Interest" Label (Bearish/Bullish styling box)
       - "PCR" label (number box)
       - Call Exits / Put Exits layout row.
       - Call ITM / Put ITM layout row.
    2. Add `id` hooks for `analytics-oi-label`, `analytics-pcr`, `analytics-call-boundary`, `analytics-put-boundary`, `analytics-call-exits`, `analytics-put-exits`, `analytics-call-itm`, `analytics-put-itm` within divs so JS can manipulate their contents.
  </action>
  <verify>grep -q "analytics-oi-label" frontend/index.html</verify>
  <done>The HTML skeleton inside the detail-modal now resembles the metric structure at the bottom of the original desktop application screenshot.</done>
</task>

<task type="auto">
  <name>Bind Analytics to the Live Detail Modal Update</name>
  <files>
    <file>frontend/app.js</file>
  </files>
  <action>
    In `updateDetailModalLive(symbol, data)`:
    1. Extract `data.analytics`
    2. Manipulate the new UI hooks. If `data.analytics.call_sum >= data.analytics.put_sum`, Label `analytics-oi-label` as "Bearish" (red background), else "Bullish" (green background).
    3. Push the `pcr` value into `analytics-pcr` (colors based on `< 1` red, `>= 1` green).
    4. Fill `analytics-call-boundary`, `analytics-put-boundary`, `analytics-call-itm`, `analytics-put-itm` matching Tkinter's logic. Output "Yes" or "No" for Exits (`Yes` if `< 0`).
  </action>
  <verify>grep -q "analytics-oi-label" frontend/app.js</verify>
  <done>Frontend logic now assigns dynamic text nodes and class names representing the logic of the Tkinter dashboard when receiving analytical frames.</done>
</task>

## Success Criteria
- [ ] Expanded Detail modal visually includes a section showing Open Interest status, ITM status, Boundary status, and Exits.
- [ ] Green/Red color coding operates dynamically based on values, keeping identical thresholds to the original Python algorithm map.
