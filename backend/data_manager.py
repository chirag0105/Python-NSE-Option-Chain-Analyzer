import logging

logger = logging.getLogger(__name__)

class DataManager:
    """In-memory cache for option chain data."""
    def __init__(self):
        self.latest_chains = {}

    def update_chain(self, symbol: str, data: dict):
        self.latest_chains[symbol] = data
        logger.debug(f"Updated cache for {symbol}")

    def get_chain(self, symbol: str):
        return self.latest_chains.get(symbol)

data_manager = DataManager()
