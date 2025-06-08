
"""
Configuration constants for the CAMS Data Manager plugin.
"""

import os

# Plugin metadata
PLUGIN_NAME = "CAMS Data Manager"
PLUGIN_DESCRIPTION = "Download and manage CAMS air quality data in QGIS"
PLUGIN_VERSION = "0.1"
PLUGIN_AUTHOR = "POLIMI"

# Default paths
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "CAMS_Data")

# CAMS API Configuration
CAMS_API_URL = "https://ads.atmosphere.copernicus.eu/api/v2"
CAMS_DATASET = "cams-europe-air-quality-reanalyses"

# Model parameter constants
VARIABLES = [
    "ammonia", "formaldehyde", "nitrogen_dioxide", "non_methane_vocs",
    "pm2p5", "pm2p5_secondary_inorganic_aerosol", "pm2p5_total_organic_matter",
    "pm10_dust", "pm10_wildfires", "sulphur_dioxide", "carbon_monoxide", 
    "glyoxal", "nitrogen_monoxide", "ozone", "pm2p5_residential_elementary_carbon", 
    "pm2p5_total_elementary_carbon", "pm10", "pm10_sea_salt_dry", "peroxyacyl_nitrates"
]

MODELS = [
    "ensemble", "emep", "match", "mocage", "silam", "dehm",
    "chimere", "lotos-euros", "minni", "monarch", "eurad-im", "gem-aq"
]

LEVELS = ["0", "50", "100", "250", "500", "750", "1000", "2000", "3000", "5000"]

DATA_TYPES = ["validated_reanalysis", "interim_reanalysis"]

# Full model area (approximate bounds)
MODEL_BOUNDS = {
    "north": 70.0,
    "south": 30.0,
    "east": 45.0,
    "west": -30.0
}

