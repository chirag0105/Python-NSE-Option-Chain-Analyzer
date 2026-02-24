import logging

logger = logging.getLogger(__name__)

class DataManager:
    """In-memory cache for option chain data."""
    def __init__(self):
        self.latest_chains = {}
        self.analytics_history = {}

    def update_chain(self, symbol: str, data: dict):
        if symbol not in self.analytics_history:
            self.analytics_history[symbol] = []
            
        # Store historical view if data has analytics payload
        if "analytics" in data and "timestamp" in data:
            snapshot = {
                "timestamp": data.get("timestamp"),
                "underlyingValue": data.get("underlyingValue"),
                "analytics": data.get("analytics")
            }
            # Add to memory limit to 500 rows
            self.analytics_history[symbol].append(snapshot)
            if len(self.analytics_history[symbol]) > 500:
                self.analytics_history[symbol].pop(0)
                
            # Embed into payload to stream down efficiently
            data["history"] = self.analytics_history[symbol]

        self.latest_chains[symbol] = data
        logger.debug(f"Updated cache for {symbol}")

    def sync_tracked_symbols(self, tracked_symbols: set):
        """Remove symbols from cache that are no longer being tracked."""
        stale = [s for s in self.latest_chains if s not in tracked_symbols]
        for s in stale:
            del self.latest_chains[s]
            self.analytics_history.pop(s, None)

    def get_chain(self, symbol: str):
        return self.latest_chains.get(symbol)

data_manager = DataManager()
