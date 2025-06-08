"""
This module handles extraction of UI parameters from the dialog.
It provides functions to collect user input from various UI elements.
"""

VARIABLE_MAP = {
    "Ammonia": "ammonia",
    "Carbon monoxide": "carbon_monoxide",
    "Formaldehyde": "formaldehyde",
    "Glyoxal": "glyoxal",
    "Nitrogen dioxide": "nitrogen_dioxide",
    "Nitrogen monoxide": "nitrogen_monoxide",
    "Non-methane VOCs": "non_methane_vocs",
    "Ozone": "ozone",
    "Particulate matter < 2.5 µm (PM2.5)": "particulate_matter_2.5um",
    "PM2.5, residential elementary carbon": "residential_elementary_carbon",
    "PM2.5, secondary inorganic aerosol": "secondary_inorganic_aerosol",
    "PM2.5, total organic matter": "pm2.5_total_organic_matter",
    "Particulate matter < 10 µm (PM10)": "particulate_matter_10um",
    "PM10, dust": "dust",
    "PM10, sea salt (dry)": "pm10_sea_salt_dry",
    "PM10, wildfires": "pm10_wildfires",
    "PM10, total elementary carbon": "pm10_total_elementary_carbon",
    "Peroxyacyl nitrates": "peroxyacyl_nitrates",
    "Sulphur dioxide": "sulphur_dioxide"
}

# Mapping from API variable name to NetCDF variable name
NETCDF_VARIABLE_MAP = {
    "ammonia": "nh3",
    "ozone": "o3",
    "nitrogen_dioxide": "no2",
    "nitrogen_monoxide": "no",
    "sulphur_dioxide": "so2",
    "carbon_monoxide": "co",
    "formaldehyde": "hcho",
    "glyoxal": "chocho",
    "non_methane_vocs": "nmvoc",
    "pm2p5": "pm2p5",
    "pm2p5_secondary_inorganic_aerosol": "pm2p5_si",
    "pm2p5_total_organic_matter": "pm2p5_om",
    "pm2p5_residential_elementary_carbon": "pm2p5_ec_res",
    "pm2p5_total_elementary_carbon": "pm2p5_ec_tot",
    "pm10": "pm10",
    "pm10_dust": "pm10_dust",
    "pm10_sea_salt_dry": "pm10_ss",
    "pm10_wildfires": "pm10_fire",
    "pm10_total_elementary_carbon": "pm10_ec_tot",
    "peroxyacyl_nitrates": "pan"
}

MODEL_MAP = {
    "Ensemble median": "ensemble",
    "CHIMERE": "chimere",
    "EMEP": "emep",
    "LOTOS-EUROS": "lotos",
    "MATCH": "match",
    "MINNI": "minni",
    "MOCAGE": "mocage",
    "MONARCH": "monarch",
    "SILAM": "silam",
    "EURAD-IM": "euradim",
    "DEHM": "dehm",
    "GEM-AQ": "gemaq"
}

TYPE_MAP = {
    "Validated reanalysis": "validated_reanalysis",
    "Interim reanalysis": "interim_reanalysis"
}

AVAILABILITY = {
    # 1. Ammonia
    ("Ammonia", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Ammonia", "MATCH", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Ammonia", "MINNI", "Interim reanalysis"): ["2023"],
    ("Ammonia", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Ammonia", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Ammonia", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ammonia", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ammonia", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Ammonia", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 2. Carbon monoxide
    ("Carbon monoxide", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Carbon monoxide", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Carbon monoxide", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Carbon monoxide", "MINNI", "Interim reanalysis"): ["2023"],
    ("Carbon monoxide", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Carbon monoxide", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Carbon monoxide", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Carbon monoxide", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Carbon monoxide", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 3. Formaldehyde
    ("Formaldehyde", "Ensemble median", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "Ensemble median", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "CHIMERE", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "CHIMERE", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "EMEP", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "EMEP", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "LOTOS-EUROS", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "LOTOS-EUROS", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "MATCH", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "MATCH", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "MINNI", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "MINNI", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "MOCAGE", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "MOCAGE", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "SILAM", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "SILAM", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "EURAD-IM", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "EURAD-IM", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "DEHM", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "DEHM", "Interim reanalysis"): ["2023"],
    ("Formaldehyde", "GEM-AQ", "Validated reanalysis"): ["2021", "2022"],
    ("Formaldehyde", "GEM-AQ", "Interim reanalysis"): ["2023"],

    # 4. Glyoxal
    ("Glyoxal", "Ensemble median", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "Ensemble median", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "CHIMERE", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "CHIMERE", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "EMEP", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "EMEP", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "LOTOS-EUROS", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "LOTOS-EUROS", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "MATCH", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "MATCH", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "MINNI", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "MINNI", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "MOCAGE", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "MOCAGE", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "SILAM", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "SILAM", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "EURAD-IM", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "EURAD-IM", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "DEHM", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "DEHM", "Interim reanalysis"): ["2023"],
    ("Glyoxal", "GEM-AQ", "Validated reanalysis"): ["2021", "2022"],
    ("Glyoxal", "GEM-AQ", "Interim reanalysis"): ["2023"],

    # 5. Nitrogen dioxide
    ("Nitrogen dioxide", "Ensemble median", "Validated reanalysis"): ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Nitrogen dioxide", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Nitrogen dioxide", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Nitrogen dioxide", "MINNI", "Interim reanalysis"): ["2023"],
    ("Nitrogen dioxide", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Nitrogen dioxide", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Nitrogen dioxide", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen dioxide", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Nitrogen dioxide", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 6. Nitrogen monoxide
    ("Nitrogen monoxide", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Nitrogen monoxide", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Nitrogen monoxide", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Nitrogen monoxide", "MINNI", "Interim reanalysis"): ["2023"],
    ("Nitrogen monoxide", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Nitrogen monoxide", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Nitrogen monoxide", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Nitrogen monoxide", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Nitrogen monoxide", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 7. Non-methane VOCs
    ("Non-methane VOCs", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Non-methane VOCs", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Non-methane VOCs", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Non-methane VOCs", "MINNI", "Interim reanalysis"): ["2023"],
    ("Non-methane VOCs", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Non-methane VOCs", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Non-methane VOCs", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Non-methane VOCs", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Non-methane VOCs", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 8. Ozone
    ("Ozone", "Ensemble median", "Validated reanalysis"): ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Ozone", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Ozone", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Ozone", "MINNI", "Interim reanalysis"): ["2023"],
    ("Ozone", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Ozone", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Ozone", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Ozone", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Ozone", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Ozone", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 9. Particulate matter < 2.5 µm (PM2.5)
    ("Particulate matter < 2.5 µm (PM2.5)", "Ensemble median", "Validated reanalysis"): ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MINNI", "Interim reanalysis"): ["2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 2.5 µm (PM2.5)", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Particulate matter < 2.5 µm (PM2.5)", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 10. PM2.5, residential elementary carbon
    ("PM2.5, residential elementary carbon", "Ensemble median", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "Ensemble median", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "CHIMERE", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "CHIMERE", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "EMEP", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "EMEP", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "LOTOS-EUROS", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "LOTOS-EUROS", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "MINNI", "Interim reanalysis"): ["2023"],
    ("PM2.5, residential elementary carbon", "MOCAGE", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "MOCAGE", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("PM2.5, residential elementary carbon", "MONARCH", "Interim reanalysis"): ["2023"],
    ("PM2.5, residential elementary carbon", "SILAM", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "SILAM", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "EURAD-IM", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "EURAD-IM", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "DEHM", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "DEHM", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, residential elementary carbon", "GEM-AQ", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, residential elementary carbon", "GEM-AQ", "Interim reanalysis"): ["2022", "2023"],

    # 11. PM2.5, secondary inorganic aerosol
    ("PM2.5, secondary inorganic aerosol", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "MINNI", "Interim reanalysis"): ["2023"],
    ("PM2.5, secondary inorganic aerosol", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "MONARCH", "Interim reanalysis"): ["2023"],
    ("PM2.5, secondary inorganic aerosol", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM2.5, secondary inorganic aerosol", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM2.5, secondary inorganic aerosol", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 12. PM2.5, total organic matter
    ("PM2.5, total organic matter", "Ensemble median", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "CHIMERE", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "EMEP", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "LOTOS-EUROS", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "MATCH", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "MINNI", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "MOCAGE", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "MONARCH", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "SILAM", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "EURAD-IM", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "DEHM", "Validated reanalysis"): ["2022"],
    ("PM2.5, total organic matter", "GEM-AQ", "Validated reanalysis"): ["2022"],

    # 13. PM10, sea salt (dry)
    ("PM10, sea salt (dry)", "Ensemble median", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "CHIMERE", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "EMEP", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "LOTOS-EUROS", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "MATCH", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "MINNI", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "MOCAGE", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "MONARCH", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "SILAM", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "EURAD-IM", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "DEHM", "Validated reanalysis"): ["2022"],
    ("PM10, sea salt (dry)", "GEM-AQ", "Validated reanalysis"): ["2022"],

    # 14. PM10, wildfires
    ("PM10, wildfires", "Ensemble median", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "CHIMERE", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "EMEP", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "LOTOS-EUROS", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, wildfires", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, wildfires", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, wildfires", "MINNI", "Interim reanalysis"): ["2023"],
    ("PM10, wildfires", "MOCAGE", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("PM10, wildfires", "MONARCH", "Interim reanalysis"): ["2023"],
    ("PM10, wildfires", "SILAM", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "EURAD-IM", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "DEHM", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, wildfires", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, wildfires", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 15. PM10, total elementary carbon
    ("PM10, total elementary carbon", "Ensemble median", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "Ensemble median", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "CHIMERE", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "CHIMERE", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "EMEP", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "EMEP", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "LOTOS-EUROS", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "LOTOS-EUROS", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "MINNI", "Interim reanalysis"): ["2023"],
    ("PM10, total elementary carbon", "MOCAGE", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "MOCAGE", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("PM10, total elementary carbon", "MONARCH", "Interim reanalysis"): ["2023"],
    ("PM10, total elementary carbon", "SILAM", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "SILAM", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "EURAD-IM", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "EURAD-IM", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "DEHM", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "DEHM", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, total elementary carbon", "GEM-AQ", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, total elementary carbon", "GEM-AQ", "Interim reanalysis"): ["2022", "2023"],

    # 16. Peroxyacyl nitrates
    ("Peroxyacyl nitrates", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Peroxyacyl nitrates", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "MINNI", "Interim reanalysis"): ["2023"],
    ("Peroxyacyl nitrates", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Peroxyacyl nitrates", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Peroxyacyl nitrates", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Peroxyacyl nitrates", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Peroxyacyl nitrates", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 17. Sulphur dioxide
    ("Sulphur dioxide", "Ensemble median", "Validated reanalysis"): ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Sulphur dioxide", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Sulphur dioxide", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Sulphur dioxide", "MINNI", "Interim reanalysis"): ["2023"],
    ("Sulphur dioxide", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Sulphur dioxide", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Sulphur dioxide", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Sulphur dioxide", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Sulphur dioxide", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 13. Particulate matter < 10 µm (PM10)
    ("Particulate matter < 10 µm (PM10)", "Ensemble median", "Validated reanalysis"): ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "MINNI", "Interim reanalysis"): ["2023"],
    ("Particulate matter < 10 µm (PM10)", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "MONARCH", "Interim reanalysis"): ["2023"],
    ("Particulate matter < 10 µm (PM10)", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("Particulate matter < 10 µm (PM10)", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("Particulate matter < 10 µm (PM10)", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],

    # 14. PM10, dust
    ("PM10, dust", "Ensemble median", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "Ensemble median", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "CHIMERE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "CHIMERE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "EMEP", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "EMEP", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "LOTOS-EUROS", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "LOTOS-EUROS", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "MATCH", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, dust", "MATCH", "Interim reanalysis"): ["2022", "2023"],
    ("PM10, dust", "MINNI", "Validated reanalysis"): ["2020", "2021", "2022"],
    ("PM10, dust", "MINNI", "Interim reanalysis"): ["2023"],
    ("PM10, dust", "MOCAGE", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "MOCAGE", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "MONARCH", "Validated reanalysis"): ["2021", "2022"],
    ("PM10, dust", "MONARCH", "Interim reanalysis"): ["2023"],
    ("PM10, dust", "SILAM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "SILAM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "EURAD-IM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "EURAD-IM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "DEHM", "Validated reanalysis"): ["2018", "2019", "2020", "2021", "2022"],
    ("PM10, dust", "DEHM", "Interim reanalysis"): ["2021", "2022", "2023"],
    ("PM10, dust", "GEM-AQ", "Validated reanalysis"): ["2019", "2020", "2021", "2022"],
    ("PM10, dust", "GEM-AQ", "Interim reanalysis"): ["2021", "2022", "2023"],
}

def collect_download_parameters(ui):
    """
    Collect all user-selected parameters from the UI.

    This function extracts values from combo boxes, checkboxes, 
    and the folder path lineEdit, returning them as a dictionary.
    It relies on the yearCheckBox and monthCheckBox dictionaries
    being already set up on the ui object.

    Parameters:
        ui (QWidget): The UI object containing the input elements
                    (typically dialog instance in cams_data_manager.py)

    Returns:
        dict: Dictionary containing selected parameter values
    """
    # Verify that checkbox dictionaries exist
    if not hasattr(ui, 'yearCheckBox') or not hasattr(ui, 'monthCheckBox'):
        # Handle the error - either create dictionaries if possible or show an error
        print("Warning: yearCheckBox or monthCheckBox dictionaries not found on UI object")
        # Try to create them if they don't exist (fallback)
        try:
            # Create year checkbox dictionary
            ui.yearCheckBox = {
                str(y): getattr(ui, f"checkYear{y}") 
                for y in range(2013, 2024) 
                if hasattr(ui, f"checkYear{y}")
            }
            
            # Create month checkbox dictionary
            ui.monthCheckBox = {
                f"{m:02}": getattr(ui, f"checkMonth{m:02}") 
                for m in range(1, 13) 
                if hasattr(ui, f"checkMonth{m:02}")
            }
        except Exception as e:
            print(f"Error creating checkbox dictionaries: {str(e)}")
    
    # Get current selections
    current_variable = ui.comboVariable.currentText()
    current_type = ui.comboType.currentText()
    
    # Special handling for variables that only have Validated reanalysis
    special_variables = ["PM10, sea salt (dry)", "PM2.5, total organic matter"]
    if current_variable in special_variables and current_type == "Interim reanalysis":
        # If user selected a special variable with Interim reanalysis,
        # show a warning message and return None
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(
            ui,
            "Invalid Selection",
            f"The variable '{current_variable}' is only available in Validated reanalysis type.\n"
            "Please select Validated reanalysis type to proceed."
        )
        return None
    
    folder = ui.lineFolder.text().strip()
    if not folder:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(ui, "Invalid Folder", "Please select a valid download folder before downloading.")
        return None
    
    # Collect all parameters into a dictionary
    params = {
        # Selected Variable (API value)
        "variable": VARIABLE_MAP.get(current_variable, ""),
        # Selected Model (API value)
        "model": MODEL_MAP.get(ui.comboModel.currentText(), ""),
        # Selected Level (e.g. 0, 500)
        "level": ui.comboLevel.currentText(),
        # Selected Type (API value)
        "type": TYPE_MAP.get(current_type, ""),
        # Selected Years: only include years where checkbox is checked
        "years": [y for y, cb in ui.yearCheckBox.items() if cb.isChecked()],
        # Selected Months: e.g. ["01", "02", ..., "12"]
        "months": [m for m, cb in ui.monthCheckBox.items() if cb.isChecked()],
        # Output folder path from lineEdit
        "folder": folder,
        # Whether user agreed to terms and conditions
        "agree_terms": ui.checkAgreement.isChecked(),
        # For the MVP, only support "full AOI" mode
        "aoi_mode": "full"
    }

    return params

