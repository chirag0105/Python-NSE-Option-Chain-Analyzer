# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.1 (Analytical Engine)

## Must-Haves (Milestone 1.1)
- [ ] Backend extracts or calculates Call Sum, Put Sum, Difference, Call Boundary, Put Boundary, Call ITM, Put ITM, PCR.
- [ ] Backend tracks the historical points throughout the day as a time-series.
- [ ] Frontend displays the time-series logs in a table view.
- [ ] Frontend displays the Bullish/Bearish layout matching the old GUI (Open Interest Boundaries, Call/Put Exits, etc).

## Phases (Milestone 1.1)

### Phase 1: Analytical Model & Time-Series State
**Status**: ⬜ Not Started
**Objective**: Update the backend data processor to calculate sum boundaries, differences, PCR, and ITM metrics using the original script's offset logics based on the ATM strike. Initialize a state history manager to keep track of these records over the session.

### Phase 2: Analytics Data Streaming
**Status**: ⬜ Not Started
**Objective**: Enhance the WebSocket broadcast payload to carry both the live option chain frame and the historical analytics arrays for the user's active symbols.

### Phase 3: GUI Analytics Dashboard
**Status**: ⬜ Not Started
**Objective**: Implement the bottom table log and the summary indicator panel for Open Interest Boundaries, PCR, and Market Exits.

---
## Archived Milestone 1.0 (Web Dashboard)

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
**Status**: ✅ Complete
**Objective**: Implement WebSockets in backend, set up in-memory cache holding the latest data states and broadcast logic.
**Requirements**: REQ-03, REQ-06

### Phase 3: Web Dashboard (Frontend)
**Status**: ✅ Complete
**Objective**: Create the Vanilla HTML/CSS/JS frontend dashboard summary structure offering adding multiple index/stock monitors.
**Requirements**: REQ-02, REQ-04

### Phase 4: Detailed View & Polish
**Status**: ✅ Complete
**Objective**: Enhance dashboard so summary cards can be expanded to full option chain views parsing data clearly. Improve styling and UX responsiveness.
**Requirements**: REQ-05
