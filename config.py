
"""Central configuration for the Forest Fire Early Warning System.

All values are read from environment variables (see .env.example).
Nothing secret is hard-coded here.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- NASA FIRMS -------------------------------------------------------
# Get a free key at https://firms.modaps.eosdis.nasa.gov/api/map_key/
FIRMS_MAP_KEY = os.getenv("FIRMS_MAP_KEY", "242260956b4813fbd374c08ad4417ef7")

# Satellite/sensor source. Common choices:
# VIIRS_SNPP_NRT, VIIRS_NOAA20_NRT, VIIRS_NOAA21_NRT, MODIS_NRT
FIRMS_SOURCE = os.getenv("FIRMS_SOURCE", "VIIRS_SNPP_NRT")

# Bounding box for Nepal: west, south, east, north
NEPAL_BBOX = os.getenv("NEPAL_BBOX", "80.0,26.3,88.3,30.5")

# How many days back to query (FIRMS allows 1-10 for the area API)
# Corrected code:
FIRMS_DAY_RANGE = int(os.getenv('FIRMS_DAY_RANGE', 1))

FIRMS_AREA_URL = (
    "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    "{map_key}/{source}/{bbox}/{days}"
)

# --- App -------------------------------------------------------------------
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"

# Map Bounding Box for Nepal [west, south, east, north]
# NEPAL_BBOX = os.getenv("NEPAL_BBOX", "80.0,26.3,88.3,30.5")
# Bounding Box for India [west, south, east, north]
NEPAL_BBOX = os.getenv("NEPAL_BBOX", "80.06, 26.36, 88.20, 30.45")



