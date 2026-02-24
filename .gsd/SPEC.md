# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
Transform the existing desktop-only Tkinter Option Chain application into a modern web-based monitoring dashboard. Users can simultaneously track multiple NSE assets (indexes and stocks) on a single screen with live, WebSocket-driven updates, removing the need to run multiple desktop instances.

## Goals
1. Replace the Tkinter UI with a web-based dashboard and an API-driven backend.
2. Enable monitoring of multiple option chains simultaneously via a centralized "Summary Dashboard" layout.
3. Stream real-time data efficiently from the backend to the frontend using WebSockets.

## Non-Goals (Out of Scope)
- Historical data analysis charting.
- Trading execution or broker integration.
- Moving away from Python for the core data fetching logic.
- Complex frontend frameworks (React/Vue/Angular); sticking to Vanilla HTML/JS/CSS.

## Users
Traders and analysts who need to efficiently monitor real-time changes across multiple NSE option chains (like NIFTY, BANKNIFTY, Reliance) without cluttering their desktop with numerous standalone windows.

## Constraints
- **Technical constraints:** Must use Vanilla HTML/CSS/JS for the frontend; Python (likely FastAPI) for the backend and WebSocket handling. Performance overhead from constant polling/ws communication must be optimized.
- **Data restrictions:** NSE's API has strict rate limits, so backend polling must be efficient and well-cached before broadcasting to WebSocket clients.

## Success Criteria
- [ ] Users can select and view at least 5 different option chains on a single webpage via a summary view dashboard.
- [ ] Users can expand a summary card to see the full detailed option chain grid.
- [ ] Option chains update automatically and continuously in the UI via WebSockets without page reloads.
- [ ] Backend makes optimal requests to NSE without getting IP-blocked.
