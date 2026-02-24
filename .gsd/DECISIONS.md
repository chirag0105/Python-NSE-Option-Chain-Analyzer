# DECISIONS

| Date | Context | Decision | Rationale | Consequences |
|------|---------|----------|-----------|--------------|
| $(Get-Date -Format 'yyyy-MM-dd') | Frontend UI Framework | Use Vanilla HTML/JS/CSS | Avoid overwhelming the architecture with React/Vue complexity right now and focus on keeping it lightweight. | Build out UI components manually using DOM querying. |
| $(Get-Date -Format 'yyyy-MM-dd') | Web Data Updates | WebSockets | Real-time option data requires low latency and should be pushed to clients rather than having them actively poll, which reduces HTTP overhead. | Requires asynchronous backend structure supporting ws (FastAPI). |
