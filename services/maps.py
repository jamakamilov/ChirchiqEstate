from config import settings
from urllib.parse import urlencode

def osm_static_map(coords: dict, zoom=16, size=(600, 400), marker=True):
    params = {
        "center": f"{coords['lat']},{coords['lon']}",
        "zoom": zoom,
        "size": f"{size[0]}x{size[1]}",
        "maptype": "mapnik"
    }
    if marker:
        params["markers"] = f"{coords['lat']},{coords['lon']},lightblue1"
    return f"{settings.OSM_STATIC_MAP_URL}?{urlencode(params)}"

def osm_link(coords: dict):
    return f"https://www.openstreetmap.org/?mlat={coords['lat']}&mlon={coords['lon']}#map=18/{coords['lat']}/{coords['lon']}"
