import cdsapi

dataset = "cams-europe-air-quality-reanalyses"
request = {
    "variable": ["ammonia"],
    "model": ["ensemble"],
    "level": ["50"],
    "type": ["validated_reanalysis"],
    "year": ["2022"],
    "month": ["01"]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download() 