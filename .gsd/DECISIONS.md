# DECISIONS

| Date | Context | Decision | Rationale | Consequences |
|------|---------|----------|-----------|--------------|
| $(Get-Date -Format 'yyyy-MM-dd') | Frontend UI Framework | Use Vanilla HTML/JS/CSS | Avoid overwhelming the architecture with React/Vue complexity right now and focus on keeping it lightweight. | Build out UI components manually using DOM querying. |
| $(Get-Date -Format 'yyyy-MM-dd') | Web Data Updates | WebSockets | Real-time option data requires low latency and should be pushed to clients rather than having them actively poll, which reduces HTTP overhead. | Requires asynchronous backend structure supporting ws (FastAPI). |
| 2026-02-24 | Backend Architecture | Option B: Clean rewrite | Extracting code from the monolithic Tkinter app is messy. A fresh FastAPI app provides a clean boundaries. | Previous data fetching/parsing logic must be re-implemented natively using modern structures. |
| 2026-02-24 | Configuration Storage | JSON files | Simple, readable format that perfectly suits small scale configuration storage without needing a database. | Must handle file locks/concurrency if multiple edits occur. |
| 2026-02-24 | Background Polling | Native `asyncio` loops via FastAPI lifespan | Avoids heavy scheduling libraries (like APScheduler) while perfectly serving endless background polling. | Requires careful error handling so the `while` loop doesn't crash silently. |
| 2026-02-24 | NSE API Session | Explicit Header/Cookie Management | NSE API has strict rate limits and requires fresh cookies. We must mimic browser headers and request the homepage first. | Increased logic needed to manage `httpx.AsyncClient` sessions and rotate/fetch headers periodically. |
