<img width="128" height="128" src="https://i.imgur.com/OGHZnUu.png" alt="icon_square">

# NSE Option Chain Analyzer — Web Edition

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A modern, real-time web dashboard for analyzing NSE Option Chains — rebuilt from the original Python/Tkinter desktop app into a FastAPI + Vanilla JS web application with live WebSocket streaming, multi-symbol tracking, and a full analytical engine.

---

## ✨ What's New (Web Version)

| Feature | Desktop (Tkinter) | Web Edition |
|---|---|---|
| Multi-symbol tracking | ❌ Single symbol | ✅ Track 5+ simultaneously |
| Real-time updates | Polling loop | ⚡ WebSocket push |
| Summary dashboard | ❌ | ✅ At-a-glance cards |
| Expanded detail view | Single window | ✅ Full modal with chain + analytics |
| Historical time-series | ✅ Table | ✅ Color-coded table with trend indicators |
| Analytics indicators | ✅ Labels | ✅ Dynamic Bullish/Bearish panels |
| Cross-platform | Windows only (.exe) | ✅ Any browser, any OS |
| Installation | Download + run | `pip install` + one command |

---

## Disclaimer

> **This software is unofficial and is not affiliated with / endorsed or approved by the National Stock Exchange (NSE) or Mr. Sameer Dharaskar in any way.**
>
> **This is purely an enthusiast program intended for educational purposes only and is not financial advice.**
>
> **By using this software you acknowledge that you are using this at your own risk and that the authors are not responsible for any damages that may occur due to the usage of this program.**
>
> **All NSE names/symbols are owned by the National Stock Exchange.**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/VarunS2002/Python-NSE-Option-Chain-Analyzer.git
cd Python-NSE-Option-Chain-Analyzer

# Install dependencies
pip install -r requirements.txt
```

### Running

```bash
python -m uvicorn backend.main:app --reload
```

Open your browser to **[http://localhost:8000](http://localhost:8000)**

---

## 📖 Usage

1. **Configure Symbols** — Click the "Configure Symbols" button in the top-right corner
2. **Select Indices or Equities** — Check the symbols you want to monitor (e.g. NIFTY, BANKNIFTY, RELIANCE)
3. **Save** — The dashboard immediately begins streaming live data via WebSocket
4. **View Summary Cards** — Each symbol gets a card displaying its current option chain snapshot
5. **Expand Detail View** — Click any symbol name to open the full analytics modal with:
   - Historical time-series log (color-coded trends)
   - Full option chain grid (Call OI, LTP, Strike, Put LTP, Put OI)
   - Analytical indicators panel (OI status, PCR, Boundaries, ITM, Exits)

---

## 🏗️ Architecture

```
Python-NSE-Option-Chain-Analyzer/
├── backend/
│   ├── main.py                 # FastAPI app, lifespan, background poller
│   ├── routers.py              # API endpoints + WebSocket handler
│   ├── nse_client.py           # HTTP/2 client for NSE API with session mgmt
│   ├── data_processor.py       # Analytical engine (PCR, Boundaries, ITM, Exits)
│   ├── data_manager.py         # In-memory cache + time-series history
│   ├── websocket_manager.py    # WebSocket connection manager + broadcast
│   ├── config_manager.py       # Persists user config to config.json
│   └── models.py               # Pydantic data models
├── frontend/
│   ├── index.html              # Dashboard structure + detail modal
│   ├── style.css               # Dark theme, glassmorphism, responsive grid
│   └── app.js                  # WebSocket client, DOM rendering, analytics binding
├── config.json                 # User configuration (tracked symbols, interval)
└── requirements.txt            # Python dependencies
```

### Data Flow

```
NSE API ──► nse_client.py ──► data_processor.py ──► data_manager.py ──► WebSocket ──► Browser
              (HTTP/2)         (Analytics calc)      (Cache + History)    (Push)       (Live render)
```

1. **Background Poller** (`main.py`) runs on a configurable interval (default: 60s)
2. **NSE Client** fetches raw option chain data with proper session/cookie management
3. **Data Processor** calculates all analytical metrics around the ATM strike
4. **Data Manager** caches the latest state + appends to a rolling 500-entry history per symbol
5. **WebSocket Manager** broadcasts the full payload to all connected clients
6. **Frontend** renders cards, populates detail modals, and color-codes historical trends

---

## 📊 Data & Analytics

### Option Chain Table

| Column | Description |
|--------|-------------|
| Call OI | Call Open Interest (with change in OI) |
| Call LTP | Call Last Traded Price |
| Strike | Strike Price (ATM highlighted) |
| Put LTP | Put Last Traded Price |
| Put OI | Put Open Interest (with change in OI) |

### Analytical Indicators

| Indicator | Description |
|-----------|-------------|
| **Open Interest** | Bullish (green) if Put Sum > Call Sum, Bearish (red) if Call Sum ≥ Put Sum |
| **PCR** | Put-Call Ratio = Total Put OI / Total Call OI. Green if ≥ 1, Red if < 1 |
| **Call Boundary** | Change in Call OI 2 strikes above ATM. Indicates if Call writers are entering (+ve, bearish) or exiting (-ve, bullish) |
| **Put Boundary** | Change in Put OI at ATM. Indicates if Put writers are entering (+ve, bullish) or exiting (-ve, bearish) |
| **Call ITM** | Ratio of Put/Call writing 4 strikes above ATM. If > 1.5, bullish signal |
| **Put ITM** | Ratio of Call/Put writing 2 strikes below ATM. If > 1.5, bearish signal |
| **Call Exits** | "Yes" if any of the 3 Call OI changes (ATM, ATM+1, ATM+2) are negative |
| **Put Exits** | "Yes" if any of the 3 Put OI changes (ATM, ATM+1, ATM+2) are negative |

### Historical Time-Series Table

Each row represents a polling snapshot with color-coded cells:
- 🟢 **Green** — Value increased from previous tick
- 🔴 **Red** — Value decreased from previous tick

Columns tracked: Time, Underlying Value, Call Sum, Put Sum, Difference, Call Boundary, Put Boundary, Call ITM, Put ITM

Calculations are based on [Mr. Sameer Dharaskar's Course](http://advancesharetrading.com/).

---

## ⚙️ Configuration

The app persists configuration to `config.json`:

```json
{
  "tracked_scripts": [
    {"symbol": "NIFTY", "type": "index"},
    {"symbol": "BANKNIFTY", "type": "index"}
  ],
  "refresh_interval": 60
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `tracked_scripts` | Array of symbols to monitor | `[]` |
| `refresh_interval` | Polling interval in seconds | `60` |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/config` | Get current configuration |
| `POST` | `/api/config` | Update tracked symbols and interval |
| `GET` | `/api/symbols` | List available indices and equities |
| `GET` | `/api/chain/{symbol}` | Get latest cached chain for a symbol |
| `WS` | `/api/ws` | WebSocket endpoint for real-time updates |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework and API routing |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [httpx](https://www.python-httpx.org/) | HTTP/2 async client for NSE API |
| [Pydantic](https://docs.pydantic.dev/) | Data validation and settings |
| [websockets](https://websockets.readthedocs.io/) | WebSocket protocol support |
| [Brotli](https://pypi.org/project/Brotli/) | Decoding compressed NSE responses |

---

## 🗂️ Version History

| Version | Description |
|---------|-------------|
| **v1.1** | Analytical Engine — PCR, Boundaries, ITM, Exits, Historical time-series, Color-coded dashboard |
| **v1.0** | Web Dashboard — Multi-symbol tracking, WebSocket streaming, Summary cards, Detail modal |
| **v5.7** (Desktop) | Original Tkinter desktop application |

---

## 🤝 Contributing

Feel free to open issues or submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0)

---

## 🙏 Credits

- Original desktop application by [VarunS2002](https://github.com/VarunS2002)
- Calculations based on [Mr. Sameer Dharaskar's Course](http://advancesharetrading.com/)
- Contributors: [medknecth](https://github.com/medknecth/), [Sangram2905](https://github.com/Sangram2905/), [yjagota](https://github.com/yjagota/), [QuickLearner171998](https://github.com/QuickLearner171998/)
