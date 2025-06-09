import sys
print("Python executable:", sys.executable)
import cdsapi
import os
import requests
from requests.exceptions import HTTPError

# Initialize cdsapi client
c = cdsapi.Client(debug=True)  # Enable debug for more information

# Print API URL from client
print("API URL:", c.url)
print("API key:", c.key)  # Will print only hash, not actual key

# Alternative approach - try direct API access
print("\nAttempting direct API request...")

# Try to get information about available datasets
try:
    # Check if we can access the Copernicus Data Space Ecosystem API
    # This URL is based on current documentation
    response = requests.get(
        'https://dataspace.copernicus.eu/api/collections/available',
        headers={
            'Accept': 'application/json'
        }
    )
    response.raise_for_status()
    print("Data Space API response:", response.status_code)
    print("Available collections:", response.json()[:5])  # Print first 5 collections
except Exception as e:
    print(f"Data Space API request failed: {str(e)}")

# Try the original request with error handling
try:
    print("\nAttempting original CAMS data retrieval...")
    result = c.retrieve(
        'cams-europe-air-quality-reanalyses',
        {
            "variable": ["ammonia"],
            "model": ["ensemble"],
            "level": ["50"],
            "type": ["validated_reanalysis"],
            "year": ["2022"],
            "month": ["01"],
            "format": "zip"
        },
        'test_download.zip'
    )
    print("Download successful:", result)
except Exception as e:
    print(f"Original request failed: {str(e)}")
    
    # Try alternative dataset name
    try:
        print("\nTrying alternative dataset name...")
        result = c.retrieve(
            'cams-european-air-quality-reanalysis',  # Try slight name variation
            {
                "variable": ["ammonia"],
                "model": ["ensemble"],
                "level": ["50"],
                "type": ["validated_reanalysis"],
                "year": ["2022"],
                "month": ["01"],
                "format": "zip"
            },
            'test_download.zip'
        )
        print("Alternative download successful:", result)
    except Exception as e2:
        print(f"Alternative request also failed: {str(e2)}")

# Your ADS account and key
email = "zhanbin.wu@mail.polimi.it"
api_key = "fb035dd1-804d-4b80-8cd0-61d31084ce2b"

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