import zipfile
import os

def unzip_and_get_netcdf(zip_path, extract_to=None):
    """
    Unzip the given ZIP file and return the path of the first NetCDF (.nc) file found.
    """
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for f in zip_ref.namelist():
            if f.endswith('.nc'):
                return os.path.join(extract_to, f)
    return None

