# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.0

## Must-Haves (from SPEC)
- [ ] Users can select and view at least 5 different option chains on a single webpage via a summary view dashboard.
- [ ] Users can expand a summary card to see the full detailed option chain grid.
- [ ] Option chains update automatically and continuously in the UI via WebSockets without page reloads.
- [ ] Backend makes optimal requests to NSE without getting IP-blocked.

## Phases

### Phase 1: Foundation (Backend & API)
**Status**: ✅ Complete
**Objective**: Build out FastAPI backend service to manage configurations, background data fetching to NSE, and exposing endpoints for available symbols/expiry dates.
**Requirements**: REQ-01, REQ-06

### Phase 2: Live Data Streaming (WebSockets)
**Status**: ⬜ Not Started
**Objective**: Implement WebSockets in backend, set up in-memory cache holding the latest data states and broadcast logic.
**Requirements**: REQ-03, REQ-06

### Phase 3: Web Dashboard (Frontend)
**Status**: ⬜ Not Started
**Objective**: Create the Vanilla HTML/CSS/JS frontend dashboard summary structure offering adding multiple index/stock monitors.
**Requirements**: REQ-02, REQ-04

### Phase 4: Detailed View & Polish
**Status**: ⬜ Not Started
**Objective**: Enhance dashboard so summary cards can be expanded to full option chain views parsing data clearly. Improve styling and UX responsiveness.
**Requirements**: REQ-05
