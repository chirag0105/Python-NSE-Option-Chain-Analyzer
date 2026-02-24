import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routers import api_router
from backend.config_manager import ConfigManager
from backend.data_manager import data_manager
from backend.nse_client import nse_client
from backend.data_processor import DataProcessor
from backend.websocket_manager import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def background_poll():
    while True:
        try:
            config = await ConfigManager.load_config()
            interval = config.refresh_interval
            
            for script in config.tracked_scripts:
                try:
                    logger.info(f"Fetching option chain for {script.symbol}")
                    data = await nse_client.fetch_option_chain(script.symbol, script.type)
                    processed = DataProcessor.process_chain(data, limit_strikes=20)
                    processed["symbol"] = script.symbol
                    data_manager.update_chain(script.symbol, processed)
                except Exception as e:
                    logger.error(f"Failed to fetch {script.symbol}: {e}")
            
            await manager.broadcast({"type": "update", "data": data_manager.latest_chains})
            await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logger.info("Background polling task cancelled.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in background polling: {e}")
            await asyncio.sleep(10)  # brief wait before retry

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize NSE session
    await nse_client.initialize_session()
    
    # Start polling loop
    poll_task = asyncio.create_task(background_poll())
    
    yield
    
    # Cleanup
    poll_task.cancel()
    await nse_client.close()

app = FastAPI(title="NSE Option Chain Analyzer API", lifespan=lifespan)
app.include_router(api_router, prefix="/api")

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
