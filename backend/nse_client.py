import httpx
import logging

logger = logging.getLogger(__name__)

class NSEClient:
    """Asynchronous client for interacting with the NSE Option Chain APIs."""
    
    BASE_URL = "https://www.nseindia.com"
    API_INDICES = "https://www.nseindia.com/api/option-chain-indices"
    API_EQUITIES = "https://www.nseindia.com/api/option-chain-equities"
    
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
    }

    def __init__(self):
        self.client = httpx.AsyncClient(headers=self.HEADERS, timeout=10.0, http2=True)
        self._session_initialized = False

    async def initialize_session(self):
        """Fetch the homepage to generate required cookies for the API routing."""
        try:
            # Drop previous cookies
            self.client.cookies.clear()
            # Hit option-chain directly as the gateway instead of the main page
            response = await self.client.get(f"{self.BASE_URL}/option-chain")
            self._session_initialized = True
            logger.info("NSE session initialized successfully via option-chain page.")
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

    async def fetch_underlying_information(self):
        """Fetch list of available indices and stocks from NSE."""
        return await self._request_with_retry(f"{self.BASE_URL}/api/underlying-information")

    async def fetch_contract_info(self, symbol: str):
        """Fetch the contract info for a given symbol to get its expiry dates."""
        return await self._request_with_retry(f"{self.BASE_URL}/api/option-chain-contract-info", params={"symbol": symbol})

    async def fetch_option_chain(self, symbol: str, type_val: str = "index"):
        """Fetch the option chain for a given symbol. type_val must be 'index' or 'stock'"""
        # NSE's V3 API requires an explicit expiry date to return data
        contract_info = await self.fetch_contract_info(symbol)
        if not contract_info or "expiryDates" not in contract_info or not contract_info["expiryDates"]:
            return {}
            
        closest_expiry = contract_info["expiryDates"][0]
        
        url = f"{self.BASE_URL}/api/option-chain-v3"
        type_param = "Indices" if type_val == "index" else "Equity"
        params = {"type": type_param, "symbol": symbol, "expiry": closest_expiry}
        
        return await self._request_with_retry(url, params=params)

    async def close(self):
        await self.client.aclose()

nse_client = NSEClient()
