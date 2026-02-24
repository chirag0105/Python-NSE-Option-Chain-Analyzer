class DataProcessor:
    @classmethod
    def process_chain(cls, raw_payload: dict, limit_strikes: int = 20) -> dict:
        if "records" not in raw_payload:
            return {}

        records = raw_payload["records"]
        data = records.get("data", [])
        underlying_value = records.get("underlyingValue", 0)
        timestamp = records.get("timestamp", "")
        
        # Determine the closest expiry
        expiry_dates = records.get("expiryDates", [])
        if not expiry_dates:
            return {}
        closest_expiry = expiry_dates[0]

        # Filter by closest expiry
        filtered_data = [row for row in data if row.get("expiryDate") == closest_expiry]

        # Sort by strike price
        filtered_data.sort(key=lambda x: x.get("strikePrice", 0))

        # Find the ATM (At-The-Money) index
        atm_index = 0
        min_diff = float("inf")
        for i, row in enumerate(filtered_data):
            diff = abs(row["strikePrice"] - underlying_value)
            if diff < min_diff:
                min_diff = diff
                atm_index = i

        # Slice `limit_strikes/2` rows above and below ATM
        half_limit = limit_strikes // 2
        start_index = max(0, atm_index - half_limit)
        end_index = min(len(filtered_data), atm_index + half_limit)
        
        sliced_data = filtered_data[start_index:end_index]

        # Format minimal options_data
        options_data = []
        for row in sliced_data:
            ce = row.get("CE", {})
            pe = row.get("PE", {})
            
            options_data.append({
                "strikePrice": row.get("strikePrice"),
                "CE": {
                    "openInterest": ce.get("openInterest", 0),
                    "changeinOpenInterest": ce.get("changeinOpenInterest", 0),
                    "totalTradedVolume": ce.get("totalTradedVolume", 0),
                    "lastPrice": ce.get("lastPrice", 0),
                    "change": ce.get("change", 0)
                },
                "PE": {
                    "openInterest": pe.get("openInterest", 0),
                    "changeinOpenInterest": pe.get("changeinOpenInterest", 0),
                    "totalTradedVolume": pe.get("totalTradedVolume", 0),
                    "lastPrice": pe.get("lastPrice", 0),
                    "change": pe.get("change", 0)
                }
            })

        return {
            "timestamp": timestamp,
            "underlyingValue": underlying_value,
            "expiryDate": closest_expiry,
            "options_data": options_data
        }
