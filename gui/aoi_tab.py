# aoi_tab.py
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class AOITab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Dynamically load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), "..", "cams_data_manager_dialog_base.ui")
        uic.loadUi(ui_path, self)

    def is_full_model_area_selected(self):
        """
        Check if the "Use full CAMS model area" radio button is selected.
        This will be True if the user selects the default global AOI.
        """
        return self.radioFullArea.isChecked()

