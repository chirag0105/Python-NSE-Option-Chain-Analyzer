from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from backend.config_manager import ConfigManager
from backend.models import AppConfig
from backend.nse_client import nse_client
from backend.websocket_manager import manager
from backend.data_manager import data_manager

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

@api_router.get("/config", response_model=AppConfig)
async def get_config():
    config = await ConfigManager.load_config()
    return config

@api_router.post("/config", response_model=AppConfig)
async def update_config(new_config: AppConfig):
    await ConfigManager.save_config(new_config)
    return new_config

@api_router.get("/symbols")
async def get_symbols():
    indices = await nse_client.fetch_indices_master()
    equities = await nse_client.fetch_equities_master()
    return {
        "indices": indices,
        "equities": equities
    }

@api_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Immediately send the currently cached data to the newly connected client
        await websocket.send_json({"type": "update", "data": data_manager.latest_chains})
        
        # Keep connection open and listen for potential messages (if future needed)
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@api_router.get("/chain/{symbol}")
async def get_chain(symbol: str):
    data = data_manager.latest_chains.get(symbol)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Symbol not yet available. Try again shortly.")
