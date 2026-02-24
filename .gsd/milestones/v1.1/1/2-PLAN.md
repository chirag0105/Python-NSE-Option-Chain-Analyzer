---
phase: 1
plan: 2
wave: 1
---

# Plan 1.2: Historical Time-Series State Manager

## Objective
The old GUI accumulated rows in a continuous table showing the analytical values over time. To emulate this, the backend needs to store an array of these `analytics` snapshots in memory for each active symbol, rather than just retaining the latest snapshot.

## Context
- `backend/data_manager.py` — Currently only stores the latest processed chain.
- Requirements — Provide a `history` array representing continuous points in time for each requested symbol, limited to the current market day session.

## Tasks

<task type="auto">
  <name>Implement Time Series Retention</name>
  <files>
    <file>backend/data_manager.py</file>
  </files>
  <action>
    Update `DataManager.update_chain()`:
    1. Create a dictionary that initializes an empty array `analytics_history[symbol]` when a symbol is observed.
    2. Extract the `analytics` dictionary and `timestamp` from the newly processed `chain_data`.
    3. Construct a snapshot `{ "timestamp": chain["timestamp"], "underlyingValue": chain["underlyingValue"], "analytics": chain["analytics"] }`.
    4. Append this snapshot to `analytics_history[symbol]`.
    5. Modify `update_chain` to attach the full history timeline `analytics_history[symbol]` into the `chain_data["history"]` attribute before it gets saved into `self.latest_chains[symbol]`.
  </action>
  <verify>python test_processor.py</verify>
  <done>The output processed payload contains `history` with historical entries of analytical data objects in chronological order.</done>
</task>

## Success Criteria
- [ ] Each chain object generated and delivered by the API includes the accrued history.
- [ ] Historical snapshots bundle timestamp, underlying value, and analytical fields together accurately.
