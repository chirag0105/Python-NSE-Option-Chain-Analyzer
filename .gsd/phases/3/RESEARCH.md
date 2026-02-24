# RESEARCH: Phase 3 - Web Dashboard (Frontend)

## Research Focus
- Best approach to serve Vanilla JS/CSS alongside the FastAPI backend.
- Designing a sleek, premium Glassmorphism architecture in plain CSS.
- Structuring State Management natively in Vanilla JavaScript.

## Findings

**1. FastAPI StaticFiles Integration**
FastAPI natively supports `from fastapi.staticfiles import StaticFiles`. By defining `app.mount("/", StaticFiles(directory="frontend", html=True), name="static")`, we can let the backend completely act as a web server pointing to the root `index.html` block while still serving `/api/*`.

**2. Modern Premium Vanilla CSS Design**
A premium dashboard look relies heavily on variables, contrast, and subtle depth.
- **Glassmorphism:** Achieved via `background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);`.
- **Dark Theme Palette:** Background: `#0f172a` (Slate), Cards: `rgba(30, 41, 59, 0.7)`, Accents: `#3b82f6` (Blue).
- **Typography:** Using a modern Google Font (e.g., 'Inter' or 'Outfit'). 
- **Dynamic CSS:** Instead of building grids statically, we will define a CSS Grid `.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }` which automatically expands based on how many NSE instances are tracked.

**3. State Management in Vanilla JS**
The app needs logic to know when the user connects for the first time.
- Read `localStorage.getItem('tracked_scripts')`.
- If missing, render a setup modal pulling from `/api/symbols`.
- If exists, POST to `/api/config` to ensure the polling backend tracks them, then connect the `WebSocket` to `/api/ws`.
- To avoid massive DOM thrashing, each Symbol card will be a fixed ID container `<div id="card-NIFTY">`. The WebSocket message loop simply selects `document.getElementById('card-' + symbol)` and updates `innerHTML` values.

## Technical Direction
- Make `frontend/` directory holding `index.html`, `style.css`, and `app.js`.
- Make `app.mount()` changes in `main.py`.
- Build CSS tokens targeting high-polish UX.
- Write explicit modular JS functions `init()`, `setupModal()`, `connectWebSocket()`, `renderCard(data)`.
