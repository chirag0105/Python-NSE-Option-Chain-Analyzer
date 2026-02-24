document.addEventListener("DOMContentLoaded", init);

let ws;
const REFRESH_INTERVAL = 10; // Default
let openDetailSymbol = null; // Track which symbol's detail modal is open

async function init() {
    setupUIBindings();

    let savedScripts = localStorage.getItem("tracked_scripts");

    if (!savedScripts || savedScripts === "[]") {
        showSetupModal();
        await populateSymbols();
    } else {
        const scripts = JSON.parse(savedScripts);
        await postConfig(scripts);
        connectWebSocket();
    }
}

function setupUIBindings() {
    document.getElementById("configure-btn").addEventListener("click", async () => {
        showSetupModal();
        await populateSymbols();
    });

    document.getElementById("save-config-btn").addEventListener("click", async () => {
        const scripts = getSelectedSymbols();
        if (scripts.length === 0) {
            alert("Please select at least one symbol.");
            return;
        }

        localStorage.setItem("tracked_scripts", JSON.stringify(scripts));
        hideSetupModal();

        // Clear dashboard visual
        document.getElementById('dashboard-container').innerHTML = '';

        await postConfig(scripts);

        if (!ws || ws.readyState !== WebSocket.OPEN) {
            connectWebSocket();
        }
    });

    document.getElementById("close-detail-btn").addEventListener("click", closeDetailModal);
    document.getElementById("detail-modal").addEventListener("click", (e) => {
        if (e.target.id === "detail-modal") {
            closeDetailModal();
        }
    });
}

function showSetupModal() {
    document.getElementById("setup-modal").classList.remove("hidden");
}

function hideSetupModal() {
    document.getElementById("setup-modal").classList.add("hidden");
}

async function populateSymbols() {
    try {
        const res = await fetch("/api/symbols");
        const data = await res.json();

        const indicesList = document.getElementById("indices-list");
        const equitiesList = document.getElementById("equities-list");

        indicesList.innerHTML = '';
        equitiesList.innerHTML = '';

        const savedScripts = JSON.parse(localStorage.getItem("tracked_scripts") || "[]");
        const isSelected = (symbol, type) => savedScripts.find(s => s.symbol === symbol && s.type === type);

        data.indices.forEach(idx => {
            const checked = isSelected(idx, 'index') ? 'checked' : '';
            indicesList.innerHTML += `
                <label>
                    <input type="checkbox" value="${idx}" data-type="index" ${checked}> ${idx}
                </label>
            `;
        });

        data.equities.forEach(eq => {
            const checked = isSelected(eq, 'stock') ? 'checked' : '';
            equitiesList.innerHTML += `
                <label>
                    <input type="checkbox" value="${eq}" data-type="stock" ${checked}> ${eq}
                </label>
            `;
        });
    } catch (e) {
        console.error("Failed to load symbols", e);
    }
}

function getSelectedSymbols() {
    const checkboxes = document.querySelectorAll("#setup-modal input[type='checkbox']:checked");
    return Array.from(checkboxes).map(cb => ({
        symbol: cb.value,
        type: cb.getAttribute("data-type")
    }));
}

async function postConfig(scripts) {
    try {
        await fetch("/api/config", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tracked_scripts: scripts,
                refresh_interval: REFRESH_INTERVAL
            })
        });
    } catch (e) {
        console.error("Failed to post configuration", e);
    }
}

function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/api/ws`;

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.type === "update" && payload.data) {
            for (const [symbol, data] of Object.entries(payload.data)) {
                if (Object.keys(data).length > 0) {
                    updateOrBuildCard(symbol, data);

                    if (openDetailSymbol === symbol) {
                        updateDetailModalLive(symbol, data);
                    }
                }
            }
        }
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected, attempting to reconnect...");
        setTimeout(() => connectWebSocket(), 5000);
    };

    ws.onerror = (err) => {
        console.error("WebSocket error:", err);
    };
}

function updateOrBuildCard(symbol, data) {
    const container = document.getElementById("dashboard-container");
    let card = document.getElementById(`card-${symbol}`);

    if (!card) {
        card = document.createElement("div");
        card.id = `card-${symbol}`;
        card.className = "card";
        container.appendChild(card);
    } else {
        card.classList.remove("flash");
        void card.offsetWidth; // Trigger DOM reflow to restart animation
        card.classList.add("flash");
    }

    let tableRows = '';
    if (data.options_data && Array.isArray(data.options_data)) {
        data.options_data.forEach(row => {
            tableRows += `
                <tr>
                    <td class="pe-data">${row.CE.openInterest}</td>
                    <td class="pe-data">${row.CE.lastPrice}</td>
                    <td class="strike-price">${row.strikePrice}</td>
                    <td class="ce-data">${row.PE.lastPrice}</td>
                    <td class="ce-data">${row.PE.openInterest}</td>
                </tr>
            `;
        });
    }

    card.innerHTML = `
        <div class="card-header" onclick="openDetailModal('${symbol}')" style="cursor: pointer;">
            <h2>${symbol}</h2>
            <div class="underlying-value">₹${data.underlyingValue}</div>
        </div>
        <div class="card-meta">
            <span>Expiry: ${data.expiryDate}</span>
            <span class="timestamp">${data.timestamp}</span>
        </div>
        <table class="options-table">
            <thead>
                <tr>
                    <th>Call OI</th>
                    <th>Call LTP</th>
                    <th class="strike-col">Strike</th>
                    <th>Put LTP</th>
                    <th>Put OI</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}

async function openDetailModal(symbol) {
    openDetailSymbol = symbol;

    // UI Setup before fetch finishes
    document.getElementById("detail-symbol-name").textContent = symbol;
    document.getElementById("detail-table-body").innerHTML = `<tr><td colspan="5" style="text-align: center;">Loading deep chain...</td></tr>`;
    document.getElementById("detail-modal").classList.remove("hidden");

    try {
        const res = await fetch(`/api/chain/${symbol}`);
        if (!res.ok) {
            console.error("Failed to load detailed chain");
            return;
        }
        const data = await res.json();
        updateDetailModalLive(symbol, data);
    } catch (e) {
        console.error("Error fetching detailed chain", e);
    }
}

function updateDetailModalLive(symbol, data) {
    if (openDetailSymbol !== symbol) return;

    document.getElementById("detail-expiry").textContent = `Expiry: ${data.expiryDate}`;
    document.getElementById("detail-timestamp").textContent = data.timestamp;
    document.getElementById("detail-underlying").textContent = `₹${data.underlyingValue}`;

    populateDetailTable(data);
}

function populateDetailTable(data) {
    const tbody = document.getElementById("detail-table-body");
    let html = '';

    if (data.options_data && Array.isArray(data.options_data)) {
        // Assume ATM is closest strike
        const atmStrike = data.options_data.reduce((prev, curr) =>
            Math.abs(curr.strikePrice - data.underlyingValue) < Math.abs(prev.strikePrice - data.underlyingValue) ? curr : prev
        ).strikePrice;

        data.options_data.forEach(row => {
            const isAtm = row.strikePrice === atmStrike;
            const trClass = isAtm ? 'class="detail-atm-row"' : '';

            html += `
                <tr ${trClass}>
                    <td class="pe-data">${row.CE.openInterest} <span style="font-size: 0.7em; opacity: 0.7;">(${row.CE.changeinOpenInterest})</span></td>
                    <td class="pe-data">${row.CE.lastPrice}</td>
                    <td class="strike-price">${row.strikePrice}</td>
                    <td class="ce-data">${row.PE.lastPrice}</td>
                    <td class="ce-data">${row.PE.openInterest} <span style="font-size: 0.7em; opacity: 0.7;">(${row.PE.changeinOpenInterest})</span></td>
                </tr>
            `;
        });
    }

    tbody.innerHTML = html;
}

function closeDetailModal() {
    openDetailSymbol = null;
    document.getElementById("detail-modal").classList.add("hidden");
}
