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
        filtered_data = [row for row in data if row.get("expiryDate") == closest_expiry or row.get("expiryDates") == closest_expiry]

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

        # Calculate total OI
        total_call_oi = sum(row.get("CE", {}).get("openInterest", 0) for row in filtered_data)
        total_put_oi = sum(row.get("PE", {}).get("openInterest", 0) for row in filtered_data)
        
        try:
            put_call_ratio = round(total_put_oi / total_call_oi, 2)
        except ZeroDivisionError:
            put_call_ratio = 0
            
        def safe_get_coi(idx, opt_type):
            if 0 <= idx < len(filtered_data):
                return filtered_data[idx].get(opt_type, {}).get("changeinOpenInterest", 0)
            return 0
            
        c1 = safe_get_coi(atm_index, "CE")
        c2 = safe_get_coi(atm_index + 1, "CE")
        c3 = safe_get_coi(atm_index + 2, "CE")
        call_sum = c1 + c2 + c3
        call_boundary = c3

        p1 = safe_get_coi(atm_index, "PE")
        p2 = safe_get_coi(atm_index + 1, "PE")
        p3 = safe_get_coi(atm_index + 2, "PE")
        put_sum = p1 + p2 + p3
        put_boundary = p1
        difference = call_sum - put_sum

        p4 = safe_get_coi(atm_index + 4, "PE")
        p5 = safe_get_coi(atm_index + 4, "CE")
        call_itm = 0.0
        if p5 != 0:
            call_itm = round(p4 / p5, 1)

        p6 = safe_get_coi(atm_index - 2, "CE")
        p7 = safe_get_coi(atm_index - 2, "PE")
        put_itm = 0.0
        if p7 != 0:
            put_itm = round(p6 / p7, 1)

        analytics = {
            "pcr": put_call_ratio,
            "call_sum": round(call_sum / 1000, 1),
            "put_sum": round(put_sum / 1000, 1),
            "difference": round(difference / 1000, 1),
            "call_boundary": round(call_boundary / 1000, 1),
            "put_boundary": round(put_boundary / 1000, 1),
            "call_itm": call_itm,
            "put_itm": put_itm
        }

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
            "analytics": analytics,
            "options_data": options_data
        }
