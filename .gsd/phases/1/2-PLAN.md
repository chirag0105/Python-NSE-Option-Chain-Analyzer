---
phase: 1
plan: 2
wave: 1
---

# Plan 1.2: NSE API Client

## Objective
Establish `NSEClient` using `httpx` and `asyncio` to reliably fetch raw Option Chain Data without 401 Unauthorized errors from NSE boundaries.

## Context
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- .gsd/phases/1/RESEARCH.md

## Tasks

<task type="auto">
  <name>Initialize NSEClient</name>
  <files>
    - backend/nse_client.py
  </files>
  <action>
    - Ensure `httpx` request library handles `brotli` content correctly since NSE uses it.
    - Create an asynchronous singleton/client `NSEClient` class that initializes an `httpx.AsyncClient`.
    - Setup default User-Agent headers mirroring a real browser (AppleWebKit/Gecko/Chrome) and standard accept languages.
    - Set up a class property that handles requesting the base page `https://www.nseindia.com/` first and saving returned cookies safely to the `AsyncClient` to fake a browser session properly.
  </action>
  <verify>python -c "import httpx"</verify>
  <done>Client class wraps `httpx.AsyncClient` securely and extracts cookies from the NSE homepage.</done>
</task>

<task type="auto">
  <name>Fetch Symbols and Data API requests</name>
  <files>
    - backend/nse_client.py
  </files>
  <action>
    - Add async `fetch_indices_master` returning the list of available indices.
    - Add async `fetch_equities_master` returning available stocks.
    - Add async `fetch_option_chain(symbol, type="index")` passing data against `https://www.nseindia.com/api/option-chain-indices?symbol={symbol}` or `equities?symbol={symbol}`.
    - Catch failures/401s specifically with an error log indicating session regeneration is needed.
  </action>
  <verify>python -c "import httpx"</verify>
  <done>Asynchronous methods return the un-processed Option Chain nested JSON accurately.</done>
</task>

## Success Criteria
- [ ] Cookies correctly initialized and saved off NSE baseline.
- [ ] Core endpoints defined for API fetching returning raw Option Chain Dictionary mappings.
