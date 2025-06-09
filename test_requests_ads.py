import requests

# Please fill in your ADS account and key
email = "zhanbin.wu@mail.polimi.it"  # Replace with your email
api_key = "fb035dd1-804d-4b80-8cd0-61d31084ce2b"           # Replace with your API key

# Correct ADS API endpoint
url = "https://ads.atmosphere.copernicus.eu/api/v2/retrieve/cams-europe-air-quality-reanalyses"

data = {
    "variable": ["ammonia"],
    "model": ["ensemble"],
    "level": ["50"],
    "type": ["validated_reanalysis"],
    "year": ["2022"],
    "month": ["01"],
    "format": "zip"
}

auth = (email, api_key)

print("Sending request to:", url)
response = requests.post(url, json=data, auth=auth)

print("Status code:", response.status_code)
print("Response headers:", response.headers)

if response.status_code == 200:
    with open("test_download.zip", "wb") as f:
        f.write(response.content)
    print("Download successful! File saved as test_download.zip")
else:
    print("Download failed!")
    print("Response text:", response.text) 