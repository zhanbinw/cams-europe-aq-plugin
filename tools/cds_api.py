"""
This module handles direct communication with the Copernicus Atmosphere Monitoring Service (CAMS)
Climate Data Store (CDS) API. It provides functions to request and download air quality data.
"""

import cdsapi
import os
import time
from typing import Callable, Optional, Dict, List, Union

def safe_filename(s):
    return s.replace(' ', '_')

def request_cams_data(params: Dict[str, Union[str, List[str]]], 
                     progress_callback: Optional[Callable[[int], None]] = None) -> str:
    """
    Make a request to the CAMS CDS API to download air quality data.
    
    Args:
        params: Dictionary containing request parameters:
            - variable: Chemical species/variable name
            - model: Model name
            - level: Vertical level
            - type: Data type
            - years: List of selected years
            - months: List of selected months
            - folder: Output directory path
        progress_callback: Optional callback function to report download progress (0-100)
        
    Returns:
        str: Path to the downloaded file
        
    Raises:
        ValueError: If required parameters are missing
        cdsapi.api.APIError: If the CDS API request fails
        IOError: If there are file system related errors
    """
    try:
        variable = params.get("variable")
        model = params.get("model")
        level = params.get("level")
        data_type = params.get("type")
        years = params.get("years", [])
        months = params.get("months", [])
        folder = params.get("folder")

        if not all([variable, model, level, data_type, years, months, folder]):
            missing = [k for k, v in {
                "variable": variable,
                "model": model,
                "level": level,
                "type": data_type,
                "years": years,
                "months": months,
                "folder": folder
            }.items() if not v]
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        safe_variable = safe_filename(variable)
        safe_model = safe_filename(model)
        year_str = "_".join(years)
        month_str = "_".join(months)
        filename = f"{safe_variable}_{safe_model}_{year_str}_{month_str}.zip"
        out_path = os.path.join(folder, filename)
        # Debug log
        print("==== Download Debug Info ====")
        print("variable:", variable)
        print("model:", model)
        print("level:", level)
        print("data_type:", data_type)
        print("years:", years)
        print("months:", months)
        print("folder:", folder)
        print("filename:", filename)
        print("out_path:", out_path)
        print("os.path.exists(folder):", os.path.exists(folder))
        print("os.access(folder, os.W_OK):", os.access(folder, os.W_OK))
        assert out_path is not None and out_path != "", "Output path is None or empty!"
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        c = cdsapi.Client()
        dataset = "cams-europe-air-quality-reanalyses"
        request = {
            "variable": [variable],
            "model": [model],
            "level": [level],
            "type": [data_type],
            "year": years,
            "month": months,
            "format": "zip"
        }
        print("API request payload:", request)
        c.retrieve(dataset, request, out_path)
        if not os.path.exists(out_path):
            raise IOError(f"Download completed but file not found at: {out_path}")
        return out_path
    except IOError as e:
        raise IOError(f"File system error: {str(e)}")
    except Exception as e:
        raise Exception(f"CDS API request failed: {str(e)}")



