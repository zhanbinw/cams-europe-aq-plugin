"""
This module handles validation of download parameters for the CAMS Data Manager plugin.
It provides functions to check that user inputs meet the requirements for CAMS API requests.
"""

from PyQt5.QtWidgets import QMessageBox

def show_error(message):
    """
    Show a warning message box with the given message.
    
    This function displays a modal warning dialog to notify the user
    about invalid parameters or missing inputs.
    
    Args:
        message: The warning message to display.
    """
    QMessageBox.warning(None, "Invalid Parameters", message)


def validate_params(params):
    """
    Validate the parameters collected from the UI before making a request.

    This function performs comprehensive validation of all parameters required
    for a successful CAMS API request, showing appropriate error messages
    to the user when validation fails.

    Args:
        params: Dictionary containing all parameters from the UI.
    
    Returns:
        True if all checks pass, False if any check fails.
    """
    # Check for required parameter fields
    # Variable selection
    if not params.get("variable"):
        show_error("Please select a variable (e.g., ozone, pm2p5).")
        return False

    # Model selection
    if not params.get("model"):
        show_error("Please select a model (e.g., ensemble, chimere).")
        return False

    # Level selection
    if not params.get("level"):
        show_error("Please select a vertical level (e.g., 0, 500 meters).")
        return False

    # Data type selection
    if not params.get("type"):
        show_error("Please select a data type (e.g., validated_reanalysis).")
        return False

    # Time period selection
    # At least one year must be selected
    if not params.get("years"):
        show_error("Please select at least one year.")
        return False

    # At least one month must be selected
    if not params.get("months"):
        show_error("Please select at least one month.")
        return False
    
    # CAMS API requires exactly one year and one month per request
    # (This check may be redundant if already performed in the UI,
    # but included here for completeness)
    if len(params.get("years", [])) > 1:
        show_error("Only one year can be selected per request.")
        return False
        
    if len(params.get("months", [])) > 1:
        show_error("Only one month can be selected per request.")
        return False

    # Output folder must be specified
    if not params.get("folder"):
        show_error("Please select a folder to save the downloaded data.")
        return False

    # Terms agreement check
    if not params.get("agree_terms", False):
        show_error("You must agree to the terms and conditions before downloading.")
        return False

    # Check area of interest parameters if using custom AOI
    if params.get("aoi_mode") == "custom":
        area = params.get("area", {})
        
        # Ensure all required coordinates are present
        if not all(k in area for k in ["north", "south", "east", "west"]):
            show_error("Missing coordinates for custom area of interest.")
            return False
            
        # Validate coordinate relationships
        if area.get("north", 90) <= area.get("south", -90):
            show_error("North latitude must be greater than South latitude.")
            return False
            
        if area.get("east", 180) <= area.get("west", -180):
            show_error("East longitude must be greater than West longitude.")
            return False
            
        # Validate coordinate ranges
        if not (-90 <= area.get("south", 0) <= 90):
            show_error("South latitude must be between -90 and 90 degrees.")
            return False
            
        if not (-90 <= area.get("north", 0) <= 90):
            show_error("North latitude must be between -90 and 90 degrees.")
            return False
            
        if not (-180 <= area.get("west", 0) <= 180):
            show_error("West longitude must be between -180 and 180 degrees.")
            return False
            
        if not (-180 <= area.get("east", 0) <= 180):
            show_error("East longitude must be between -180 and 180 degrees.")
            return False

    # All checks passed
    return True

