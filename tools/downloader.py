"""
This module handles the download functionality for CAMS data.
It provides functions to submit requests to the CDS API and manage the download process.
"""

from .cds_api import request_cams_data
from PyQt5.QtWidgets import QMessageBox

def submit_cams_request(params):
    """
    Submit a request to download CAMS data.

    Args:
        params (dict): Dictionary containing all parameters for the CAMS API request

    Returns:
        str: Path to the downloaded file if successful, None if failed

    Raises:
        Exception: If the download fails for any reason
    """
    try:
        print("Sending request with params:", params)
        output_file = request_cams_data(params)
        return output_file
    except Exception as e:
        print(f"Download failed: {str(e)}")
        QMessageBox.critical(
            None,
            "Download Failed",
            f"An error occurred while downloading data:\n{str(e)}"
        )
        return None

