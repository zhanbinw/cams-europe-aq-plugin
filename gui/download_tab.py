"""
This module implements the Download tab functionality for the CAMS Data Manager plugin.
It handles the UI interactions and download process for CAMS data.
"""

import os
import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QProgressDialog

# Import helper modules
from ..tools.ui_handler import collect_download_parameters, AVAILABILITY
from ..tools.downloader import submit_cams_request
from ..tools.validator import validate_params


class DownloadTab(QWidget):
    """
    Download tab implementation for the CAMS Data Manager plugin.
    
    This class manages the Download tab UI and functionality, allowing users
    to select parameters and download CAMS air quality data.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the Download tab.
        
        Args:
            parent: Parent widget, typically the main dialog.
        """
        super().__init__(parent)

        # Load the UI file - we're loading the full UI for development purposes,
        # but in a production environment, we'd create a separate UI file for just this tab
        ui_path = os.path.join(os.path.dirname(__file__), "..", "cams_data_manager_dialog_base.ui")
        uic.loadUi(ui_path, self)

        # Check if yearCheckBox and monthCheckBox dictionaries already exist
        # (they might have been created by the main dialog)
        if not hasattr(self, "yearCheckBox") or not self.yearCheckBox:
            self.setup_checkbox_dictionaries()

        # Populate dropdown combo boxes with available options
        self.populate_comboboxes()

        # Connect the Download button to its handler
        self.btnDownload.clicked.connect(self.on_btnDownload_clicked)

        # Connect variable, model, and type change signals to update year options
        self.comboVariable.currentIndexChanged.connect(self.update_year_options)
        self.comboModel.currentIndexChanged.connect(self.update_year_options)
        self.comboType.currentIndexChanged.connect(self.update_year_options)
        self.update_year_options()

    def setup_checkbox_dictionaries(self):
        """
        Create dictionaries for year and month checkboxes.
        
        This method builds dictionaries that map year and month strings to their
        corresponding checkbox widgets, making them easier to access programmatically.
        Only called if the dictionaries don't already exist.
        """
        # Create year checkbox dictionary (2013-2023)
        self.yearCheckBox = {
            str(y): getattr(self, f"checkYear{y}", None) 
            for y in range(2013, 2024) 
            if hasattr(self, f"checkYear{y}")
        }

        # Create month checkbox dictionary (01-12)
        self.monthCheckBox = {
            f"{m:02}": getattr(self, f"checkMonth{m:02}", None) 
            for m in range(1, 13) 
            if hasattr(self, f"checkMonth{m:02}")
        }

    def populate_comboboxes(self):
        """
        Fill the parameter combo boxes with available options matching the Copernicus CAMS website.
        """
        # Variable options
        self.comboVariable.clear()
        self.comboVariable.addItems([
            "Ammonia", "Carbon monoxide", "Formaldehyde", "Glyoxal", "Nitrogen dioxide",
            "Nitrogen monoxide", "Non-methane VOCs", "Ozone",
            "Particulate matter < 2.5 µm (PM2.5)", "PM2.5, residential elementary carbon",
            "PM2.5, secondary inorganic aerosol", "PM2.5, total organic matter",
            "Particulate matter < 10 µm (PM10)", "PM10, dust", "PM10, sea salt (dry)",
            "PM10, wildfires", "PM10, total elementary carbon", "Peroxyacyl nitrates", "Sulphur dioxide"
        ])

        # Model options
        self.comboModel.clear()
        self.comboModel.addItems([
            "Ensemble median", "CHIMERE", "EMEP", "LOTOS-EUROS", "MATCH", "MINNI",
            "MOCAGE", "MONARCH", "SILAM", "EURAD-IM", "DEHM", "GEM-AQ"
        ])

        # Level options
        self.comboLevel.clear()
        self.comboLevel.addItems([
            "0", "50", "100", "250", "500", "750", "1000", "2000", "3000", "5000"
        ])

        # Type options
        self.comboType.clear()
        self.comboType.addItems([
            "Validated reanalysis", "Interim reanalysis"
        ])

    def on_btnDownload_clicked(self):
        """
        Handler for the Download button click event.
        
        This method collects parameters from the UI, validates them,
        and initiates the download process.
        """
        # Check if the .cdsapirc file exists in the user's home directory
        cdsapirc_path = os.path.expanduser("~/.cdsapirc")
        if not os.path.exists(cdsapirc_path):
            QMessageBox.warning(
                self,
                "API Key Missing",
                "Please enter your API KEY in the Help tab and click Save before downloading."
            )
            return

        # Collect parameters from the UI
        params = collect_download_parameters(self)

        # Validate parameters
        if not validate_params(params):
            return  # Stop if validation fails 

        # Check agreement to terms
        if not params.get("agree_terms", False):
            QMessageBox.warning(
                self,
                "Terms Not Accepted",
                "You must agree to the terms and conditions before downloading."
            )
            return

        # Year must have only one selection
        if len(params['years']) != 1:
            QMessageBox.warning(self, "Invalid Year Selection", "Please select exactly ONE year.")
            return

        # Month must have only one selection
        if len(params['months']) != 1:
            QMessageBox.warning(self, "Invalid Month Selection", "Please select exactly ONE month.")
            return

        # Show progress dialog
        progress = QProgressDialog("Downloading data...", "Cancel", 0, 0, self)
        progress.setWindowTitle("Please wait")
        progress.setModal(True)
        progress.show()

        # Attempt download
        try:
            # Execute the download request
            submit_cams_request(params)

            # Log the download
            self.log_download(params, success=True)

            # Show success message
            QMessageBox.information(
                self,
                "Download Complete",
                "Data downloaded successfully!"
            )
        except Exception as e:
            # Log the error
            self.log_download(params, success=False, error=str(e))

            # Show error message
            QMessageBox.critical(
                self,
                "Download Failed",
                f"An error occurred:\n{str(e)}"
            )
        finally:
            # Close the progress dialog
            progress.close()

    def log_download(self, params, success=True, error=None):
        """
        Log download attempt details to a file.
        
        Args:
            params: Dictionary containing download parameters.
            success: Boolean indicating if the download was successful.
            error: Error message if the download failed.
        """
        log_path = os.path.expanduser("~/cams_plugin.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"Timestamp: {datetime.datetime.now()}\n")
            f.write(f"Status: {'Success' if success else 'Failed'}\n")
            f.write(f"Variable: {params.get('variable')}\n")
            f.write(f"Model: {params.get('model')}\n")
            f.write(f"Years: {params.get('years')}\n")
            f.write(f"Months: {params.get('months')}\n")
            f.write(f"Folder: {params.get('folder')}\n")
            if error:
                f.write(f"Error: {error}\n")
            f.write("\n")

    def update_year_options(self):
        """
        Enable only the years available for the selected Variable, Model, and Type.
        """
        var = self.comboVariable.currentText()
        model = self.comboModel.currentText()
        typ = self.comboType.currentText()
        years = AVAILABILITY.get((var, model, typ), [])
        for year, cb in self.yearCheckBox.items():
            cb.setEnabled(year in years)
            if year not in years:
                cb.setChecked(False)

