from fastapi import APIRouter
from backend.config_manager import ConfigManager
from backend.models import AppConfig
from backend.nse_client import nse_client

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
