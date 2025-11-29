def validate_price(value: str):
    try:
        v = float(value.replace(",", "").strip())
        return v if v >= 0 else None
    except:
        return None


def validate_coords(lat: str, lon: str):
    try:
        la = float(lat)
        lo = float(lon)
        if -90 <= la <= 90 and -180 <= lo <= 180:
            return {"lat": la, "lon": lo}
    except:
        return None
