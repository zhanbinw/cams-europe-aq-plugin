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

