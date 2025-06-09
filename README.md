# CAMS Europe AQ Data Manager

A QGIS plugin for downloading and analyzing CAMS European air quality reanalysis (EAC4) data.  

---

## 🌍 Dataset Supported

This plugin specifically supports data from:

**CAMS European air quality reanalyses**  
🔗 [https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-europe-air-quality-reanalyses](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-europe-air-quality-reanalyses)

---

## 🧭 Features

- AOI selection (including selected GPKG features)
- Parameter configuration (pollutant, model, level, date)
- Download data via CAMS API
- Temporal aggregation (daily, monthly, seasonal)
- Basic statistics (mean, min, max, std. dev.)
- Bivariate analysis (e.g., correlation)
- QGIS integration and visualization
- Terms and Conditions link included

---

## ⚙️ Installation

### Option 1: Manual Installation

1. Clone or download this repository
2. Copy the entire folder into your QGIS plugins directory:

```bash
# Typical plugin path for Windows:
C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins

# For macOS or Linux:
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins

Welcome to the CAMS Data Manager Plugin!
This plugin allows you to connect to the Copernicus Atmosphere Monitoring Service (CAMS) and download atmospheric data for use in QGIS.

1.Requirements:
- QGIS installed
- Python environment accessible to QGIS
- Required packages:
    pip install cdsapi pyproj rioxarray geopandas netCDF4 h5netcdf cftime h5py dask

2.How to Get Your API Key:
To connect to the CAMS API, you need to get your personal access token.
Follow these steps:
1. Visit https://ads.atmosphere.copernicus.eu/
2. Register or log in
3. Click your username (top right corner), then click the “API” tab
4. Click “Refresh API Token”
5. Copy the newly generated token in this format:(for example:fb035dd1-804d-4b80-8cd0-61d31084ce2b)
6. Paste it into the plugin field and click “Save”
⚠️ Important: Make sure to click “Refresh” before copying the token. Otherwise, it may be invalid.

3.Using the Plugin: 
- Step 1: Select your AOI (Area of Interest)
- Step 2: Choose parameters (Variable, Model, Type, Level)
- Step 3: Select date and output format
- Step 4: Accept CAMS terms and conditions
- Step 5: Click [Download]
⚠️ Note: For now, only one month of data can be downloaded per click.
To get multiple months, you can:
- Click [Download] again after each download finishes, or
- Use the CAMS ADS website: https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-reanalyses?tab=download

4.Logs: Logs are saved in your home directory as: cams_plugin.log

If you need help, Please contact: zhanbin.wu@mail.polimi.it
