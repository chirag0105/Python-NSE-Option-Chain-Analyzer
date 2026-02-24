import httpx
import logging

logger = logging.getLogger(__name__)

class NSEClient:
    """Asynchronous client for interacting with the NSE Option Chain APIs."""
    
    BASE_URL = "https://www.nseindia.com"
    API_INDICES = "https://www.nseindia.com/api/option-chain-indices"
    API_EQUITIES = "https://www.nseindia.com/api/option-chain-equities"
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    def __init__(self):
        self.client = httpx.AsyncClient(headers=self.HEADERS, timeout=10.0, http2=True)
        self._session_initialized = False

    async def initialize_session(self):
        """Fetch the homepage to generate required cookies for the API routing."""
        try:
            response = await self.client.get(self.BASE_URL)
            response.raise_for_status()
            self._session_initialized = True
            logger.info("NSE session initialized successfully via homepage.")
        except Exception as e:
            logger.error(f"Failed to initialize NSE session: {e}")
            self._session_initialized = False

    async def _request_with_retry(self, url: str, params: dict = None) -> dict:
        if not self._session_initialized:
            await self.initialize_session()
            
        try:
            response = await self.client.get(url, params=params)
            
            # If 401 Unauthorized, regenerate session and retry once
            if response.status_code == 401:
                logger.warning("Received 401 Unauthorized, re-initializing session...")
                self.client.cookies.clear()
                await self.initialize_session()
                response = await self.client.get(url, params=params)
                
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during NSE API call: {e}")
            raise

    async def fetch_indices_master(self):
        """Fetch list of available indices from NSE."""
        return await self._request_with_retry(f"{self.BASE_URL}/api/equity-master")

    async def fetch_equities_master(self):
        """Fetch list of available stock equities from NSE."""
        return await self._request_with_retry(f"{self.BASE_URL}/api/equity-stock")

    async def fetch_option_chain(self, symbol: str, type_val: str = "index"):
        """Fetch the option chain for a given symbol. type_val must be 'index' or 'stock'"""
        if type_val == "index":
            url = self.API_INDICES
        else:
            url = self.API_EQUITIES
            
        params = {"symbol": symbol}
        return await self._request_with_retry(url, params=params)

    async def close(self):
        await self.client.aclose()

nse_client = NSEClient()
