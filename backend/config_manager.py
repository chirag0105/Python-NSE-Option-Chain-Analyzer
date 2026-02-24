import json
import os
import asyncio
from backend.models import AppConfig

CONFIG_FILE = "config.json"

class ConfigManager:
    """Manages reading and writing application configuration to disk asynchronously."""
    
    @staticmethod
    async def load_config() -> AppConfig:
        if not os.path.exists(CONFIG_FILE):
            default_config = AppConfig()
            await ConfigManager.save_config(default_config)
            return default_config
        
        loop = asyncio.get_event_loop()
        def _read():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
                
        try:
            data = await loop.run_in_executor(None, _read)
            return AppConfig(**data)
        except Exception:
            return AppConfig()

    @staticmethod
    async def save_config(config: AppConfig):
        def _write():
            with open(CONFIG_FILE, "w") as f:
                json.dump(config.model_dump(), f, indent=4)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _write)
