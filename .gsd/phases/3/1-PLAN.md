---
phase: 3
plan: 1
wave: 1
---

# Plan 3.1: FastAPI `StaticFiles` Mounting and UI Shell

## Objective
Establish the frontend directory correctly linked to the FastAPI application while defining the base `index.html` structure and high-quality Glassmorphic `style.css`.

## Context
- .gsd/ROADMAP.md
- .gsd/phases/3/RESEARCH.md
- backend/main.py

## Tasks

<task type="auto">
  <name>FastAPI StaticFiles Mount</name>
  <files>
    - backend/main.py
  </files>
  <action>
    - Ensure a new directory `frontend/` sits in the project root.
    - Inside `backend/main.py`, from `fastapi.staticfiles` import `StaticFiles`.
    - Directly above `app.include_router(api_router)`, define `app.mount("/", StaticFiles(directory="frontend", html=True), name="static")` so hitting the port directly serves `index.html`.
  </action>
  <verify>python -c "from fastapi.staticfiles import StaticFiles"</verify>
  <done>FastAPI successfully mapped `/` natively pointing towards the HTML directory.</done>
</task>

<task type="manual">
  <name>Vanilla Styles and HTML Skeleton</name>
  <files>
    - frontend/index.html
    - frontend/style.css
  </files>
  <action>
    - Build `index.html` referencing `style.css` and `app.js`. Include fonts (Google Fonts: Inter + Outfit).
    - Establish a main `<div id="app">` housing a Header, a `<main id="dashboard-container">` grid, and an isolated `<div id="setup-modal">` for symbol selection.
    - Build `style.css` strictly enforcing a **WOW FACTOR** premium dark mode.
    - Set CSS Variables for a Deep Slate palette (`#0f172a`, `rgba(30, 41, 59, 0.7)` card bgs) with bright Neon Blue/Purple gradient accents (`#3b82f6` to `#8b5cf6`).
    - Define Glassmorphism tokens (`backdrop-filter`, `box-shadow: 0 4px 30px rgba(0,0,0,0.1)`).
    - Insert hover micro-animations (`transition: transform 0.2s cubic-bezier(...)`).
    - Define responsive CSS Grids for `.dashboard-container`.
  </action>
  <verify>python -c "import os; print(os.path.exists('frontend/style.css'))"</verify>
  <done>Frontend skeleton successfully presents a visually stunning layout block upon loading `localhost` without any data logic.</done>
</task>

## Success Criteria
- [ ] Root endpoint `/` cleanly serves HTML instead of 404s.
- [ ] CSS uses variables perfectly mimicking modern design trends.
- [ ] The semantic HTML layout is established for the JS engine to bind to.
