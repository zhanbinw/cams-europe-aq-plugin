import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
import xarray as xr
import logging

class AnalysisTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "..", "cams_data_manager_dialog_base.ui")
        uic.loadUi(ui_path, self)

        # Populate NetCDF file list
        self.populate_netcdf_list()
        # Connect aggregate button
        self.btnAggregate.clicked.connect(self.on_aggregate_clicked)
        # Connect browse button (optional)
        if hasattr(self, 'btnBrowseOutput'):
            self.btnBrowseOutput.clicked.connect(self.on_browse_output)
        # Connect statistics button
        self.setup_stats_connections()
        # Connect bivariate analysis button
        self.setup_bivariate_connections()

    def refresh(self):
        """
        Unified refresh for all contents in the Analysis tab, convenient for future extension.
        """
        self.populate_netcdf_list()
        self.populate_stats_layer_combo()
        self.populate_bivariate_vars()
        # Future: refresh statistics variables, clear results, etc.

    def populate_netcdf_list(self):
        self.listNetcdfLayers.clear()
        netcdf_dir = os.path.expanduser("~/CAMS_Data")
        if not os.path.exists(netcdf_dir):
            os.makedirs(netcdf_dir, exist_ok=True)
        for fname in os.listdir(netcdf_dir):
            if fname.endswith(".nc"):
                self.listNetcdfLayers.addItem(os.path.join(netcdf_dir, fname))

    def populate_stats_layer_combo(self):
        """
        Populate the comboStatsLayer dropdown to show all NetCDF files.
        """
        if hasattr(self, 'comboStatsLayer'):
            self.comboStatsLayer.clear()
            netcdf_dir = os.path.expanduser("~/CAMS_Data")
            if not os.path.exists(netcdf_dir):
                os.makedirs(netcdf_dir, exist_ok=True)
            for fname in os.listdir(netcdf_dir):
                if fname.endswith(".nc"):
                    self.comboStatsLayer.addItem(os.path.join(netcdf_dir, fname))

    def populate_bivariate_vars(self):
        """
        Populate primary/secondary variable dropdowns, by default read all variables from the first NetCDF file.
        """
        if hasattr(self, 'comboPrimaryVar') and hasattr(self, 'comboSecondaryVar'):
            self.comboPrimaryVar.clear()
            self.comboSecondaryVar.clear()
            # Default use comboStatsLayer current file
            file_path = self.comboStatsLayer.currentText().strip() if hasattr(self, 'comboStatsLayer') else None
            if not file_path or not os.path.exists(file_path):
                return
            try:
                ds = xr.open_dataset(file_path)
                var_names = list(ds.data_vars.keys())
                for v in var_names:
                    self.comboPrimaryVar.addItem(v)
                    self.comboSecondaryVar.addItem(v)
            except Exception as e:
                logging.exception("Failed to populate bivariate variable combos")

    def get_selected_stats(self):
        stats = []
        if self.checkMean.isChecked():
            stats.append('mean')
        if self.checkMax.isChecked():
            stats.append('max')
        if self.checkMin.isChecked():
            stats.append('min')
        if self.checkStd.isChecked():
            stats.append('std')
        return stats

    def run_statistics(self):
        file_path = self.comboStatsLayer.currentText().strip()
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "No file selected", "Please select a valid NetCDF file.")
            return
        stats = self.get_selected_stats()
        if not stats:
            QMessageBox.warning(self, "No statistics selected", "Please select at least one statistic.")
            return
        try:
            ds = xr.open_dataset(file_path)
            var_name = [v for v in ds.data_vars][0]  # Default first variable
            data = ds[var_name]
            results = []
            if 'mean' in stats:
                results.append(f"Mean: {float(data.mean().values):.4f}")
            if 'max' in stats:
                results.append(f"Max: {float(data.max().values):.4f}")
            if 'min' in stats:
                results.append(f"Min: {float(data.min().values):.4f}")
            if 'std' in stats:
                results.append(f"Std. Dev: {float(data.std().values):.4f}")
            self.textStatsResult.setPlainText("\n".join(results))
        except Exception as e:
            logging.exception("Statistics computation failed")
            QMessageBox.critical(self, "Statistics Failed", f"Error: {str(e)}")

    def setup_stats_connections(self):
        if hasattr(self, 'btnRunStats'):
            self.btnRunStats.clicked.connect(self.run_statistics)

    def on_browse_output(self):
        from PyQt5.QtWidgets import QFileDialog
        out_path, _ = QFileDialog.getSaveFileName(self, "Select Output NetCDF File", "", "NetCDF Files (*.nc)")
        if out_path:
            self.lineOutputPath.setText(out_path)

    def on_aggregate_clicked(self):
        # 1. Get selected NetCDF files
        selected_items = self.listNetcdfLayers.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No file selected", "Please select at least one NetCDF file.")
            return
        file_paths = [item.text() for item in selected_items]

        # 2. Get aggregation type
        agg_type = self.comboAggType.currentText()
        agg_map = {
            "Daily": "1D",
            "Weekly": "1W",
            "Monthly": "1M",
            "Quarterly": "1Q",
            "Yearly": "1Y"
        }
        resample_str = agg_map.get(agg_type, "1M")

        # 3. Get output path
        output_path = self.lineOutputPath.text().strip()
        if not output_path:
            QMessageBox.warning(self, "No output path", "Please specify an output file path.")
            return

        # Aggregate multiple files
        try:
            self.progressBarAgg.setRange(0, 0)
            # Merge all selected NetCDF files
            ds = xr.open_mfdataset(file_paths, combine='by_coords')
            # Assume variable name is the first non-coordinate variable
            var_name = [v for v in ds.data_vars][0]
            # Aggregate by time
            agg_ds = ds.resample(time=resample_str).mean()
            agg_ds.to_netcdf(output_path)
            self.progressBarAgg.setRange(0, 100)
            self.progressBarAgg.setValue(100)
            # Optional: automatically load to QGIS
            if hasattr(self, 'checkLoadToQgis') and self.checkLoadToQgis.isChecked():
                # Here you can call the main program's load NetCDF method
                pass
            QMessageBox.information(self, "Aggregation Complete", f"Aggregated file saved to:\n{output_path}")
        except Exception as e:
            self.progressBarAgg.setRange(0, 100)
            self.progressBarAgg.setValue(0)
            logging.exception("Aggregation failed")
            QMessageBox.critical(self, "Aggregation Failed", f"Error: {str(e)}")

    def run_bivariate_analysis(self):
        if not hasattr(self, 'comboPrimaryVar') or not hasattr(self, 'comboSecondaryVar'):
            return
        file_path = self.comboStatsLayer.currentText().strip() if hasattr(self, 'comboStatsLayer') else None
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "No file selected", "Please select a valid NetCDF file.")
            return
        var1 = self.comboPrimaryVar.currentText()
        var2 = self.comboSecondaryVar.currentText()
        method = self.comboAnalysisMethod.currentText() if hasattr(self, 'comboAnalysisMethod') else "Correlation"
        if not var1 or not var2:
            QMessageBox.warning(self, "No variable selected", "Please select both primary and secondary variables.")
            return
        try:
            ds = xr.open_dataset(file_path)
            data1 = ds[var1].values.flatten()
            data2 = ds[var2].values.flatten()
            import numpy as np
            mask = ~np.isnan(data1) & ~np.isnan(data2)
            data1 = data1[mask]
            data2 = data2[mask]
            if method == "Correlation":
                from scipy.stats import pearsonr
                if len(data1) == 0 or len(data2) == 0:
                    self.textBivariateResult.setPlainText("No valid data for correlation.")
                    return
                corr, pval = pearsonr(data1, data2)
                result = f"Pearson correlation: {corr:.4f}\np-value: {pval:.4g}"
                self.textBivariateResult.setPlainText(result)
            elif method == "Linear Regression":
                from scipy.stats import linregress
                if len(data1) == 0 or len(data2) == 0:
                    self.textBivariateResult.setPlainText("No valid data for regression.")
                    return
                reg = linregress(data1, data2)
                result = (
                    f"Linear regression:\n"
                    f"y = {reg.slope:.4f} * x + {reg.intercept:.4f}\n"
                    f"R² = {reg.rvalue**2:.4f}\n"
                    f"p-value = {reg.pvalue:.4g}\n"
                    f"StdErr = {reg.stderr:.4g}"
                )
                self.textBivariateResult.setPlainText(result)
            elif method == "Classification Accuracy":
                try:
                    from sklearn.metrics import accuracy_score
                except ImportError:
                    self.textBivariateResult.setPlainText("scikit-learn is required for classification accuracy analysis.")
                    return
                if len(data1) == 0 or len(data2) == 0:
                    self.textBivariateResult.setPlainText("No valid data for classification accuracy.")
                    return
                # Try to convert data to integer or string labels
                try:
                    y_true = data1.astype(int)
                    y_pred = data2.astype(int)
                except Exception:
                    y_true = data1.astype(str)
                    y_pred = data2.astype(str)
                acc = accuracy_score(y_true, y_pred)
                result = (
                    f"Classification accuracy: {acc:.4f}\n"
                    f"Total samples: {len(y_true)}"
                )
                self.textBivariateResult.setPlainText(result)
            else:
                self.textBivariateResult.setPlainText("This analysis method is not implemented yet.")
        except Exception as e:
            logging.exception("Bivariate analysis failed")
            QMessageBox.critical(self, "Bivariate Analysis Failed", f"Error: {str(e)}")

    def setup_bivariate_connections(self):
        if hasattr(self, 'btnRunBivariate'):
            self.btnRunBivariate.clicked.connect(self.run_bivariate_analysis)
