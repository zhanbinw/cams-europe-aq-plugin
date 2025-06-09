import subprocess
import importlib

def ensure_package(pkg_name):
    try:
        importlib.import_module(pkg_name)
        print(f"✅ {pkg_name} is already installed.")
    except ImportError:
        print(f"📦 Installing {pkg_name} ...")
        subprocess.check_call(["pip", "install", pkg_name])

ensure_package("xarray")
ensure_package("netCDF4")