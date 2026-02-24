---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Analytical Model & Computation Logic

## Objective
Update the `backend/data_processor.py` to calculate the same Open Interest, bounds, and PCR analytics that the original `NSE_Option_Chain_Analyzer.py` provided. These metrics should be computed relative to the At-The-Money (ATM) strike during the frame parsing.

## Context
- `NSE_Option_Chain_Analyzer.py` (Lines 1500-1560) — specifically how `c1..c3` and `p1..p7` offsets were calculated based on the ATM Strike Price index.
- `backend/data_processor.py` — Location for appending the new output payload metrics.

## Tasks

<task type="auto">
  <name>Implement Analytics Computation</name>
  <files>
    <file>backend/data_processor.py</file>
  </files>
  <action>
    Update `DataProcessor.process_chain()`:
    1. Calculate `total_call_oi` and `total_put_oi` by summing the `openInterest` for ALL CE and PE objects in the raw chain data array respectively.
    2. Then, inside the `process_chain` method where `atm_index` is located, map the relative `Change in Open Interest` offsets equivalent to the original Pandas script.
       - Note: The original index was ordered by Strike Price ascending. Our `filtered_data` array is also sorted that way.
       - Use `atm_index` to fetch the specific `ChangeinOpenInterest` (`CE.changeinOpenInterest` / `PE.changeinOpenInterest`):
         - `c1` = CE Change in OI at `atm_index`
         - `c2` = CE Change in OI at `atm_index + 1`
         - `c3` = CE Change in OI at `atm_index + 2`
         - `call_sum` = `c1 + c2 + c3`
         - `call_boundary` = `c3`
         - `p1` = PE Change in OI at `atm_index`
         - `p2` = PE Change in OI at `atm_index + 1`
         - `p3` = PE Change in OI at `atm_index + 2`
         - `put_sum` = `p1 + p2 + p3`
         - `put_boundary` = `p1`
         - `difference` = `call_sum - put_sum`
         - `p4` = PE Change in OI at `atm_index + 4`
         - `p5` = CE Change in OI at `atm_index + 4`
         - `call_itm` = `p4 / p5` (handle DivByZero)
         - `p6` = CE Change in OI at `atm_index - 2`
         - `p7` = PE Change in OI at `atm_index - 2`
         - `put_itm` = `p6 / p7` (handle DivByZero)
    3. Calculate PCR (`put_call_ratio = total_put_oi / total_call_oi`).
    4. Inject these discrete calculated values into a new top-level `analytics` dictionary object in the returned JSON structure.
  </action>
  <verify>python test_processor.py | grep -i "analytics"</verify>
  <done>The processor outputs an `analytics` key populated with exactly `call_sum`, `put_sum`, `difference`, `call_boundary`, `put_boundary`, `call_itm`, `put_itm`, and `pcr`.</done>
</task>

## Success Criteria
- [ ] Analytics math correctly matches the offset requirements relative to the ATM index.
- [ ] Safe dictionary access handles OutOfBounds errors if the ATM is too close to the edge of the chain.
- [ ] The core `output` payload provides a clean `analytics` object.
