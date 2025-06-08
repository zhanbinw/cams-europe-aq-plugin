import xarray as xr
import geopandas as gpd

def clip_netcdf_by_bbox(input_nc, output_nc, north, south, east, west):
    """
    Clip a NetCDF file to the specified latitude/longitude bounding box.
    Args:
        input_nc: Input NetCDF file path
        output_nc: Output NetCDF file path
        north, south, east, west: Bounding box (float)
    """
    ds = xr.open_dataset(input_nc)
    # Automatically detect variable names
    lat_name = 'latitude' if 'latitude' in ds.dims else 'lat'
    lon_name = 'longitude' if 'longitude' in ds.dims else 'lon'
    # NetCDF latitude is usually in descending order (north to south), slice order needs to be reversed
    clipped = ds.sel(
        **{
            lat_name: slice(north, south),
            lon_name: slice(west, east)
        }
    )
    # If clipped result is empty, raise an exception
    if clipped[lat_name].size == 0 or clipped[lon_name].size == 0:
        ds.close()
        clipped.close()
        raise ValueError("Clipped NetCDF is empty. Please check your AOI.")
    clipped.to_netcdf(output_nc)
    ds.close()
    clipped.close()

def clip_netcdf_by_shapefile(input_nc, output_nc, shapefile_path):
    """
    Clip a NetCDF file using the true polygon mask of a shapefile.
    Args:
        input_nc: Input NetCDF file path
        output_nc: Output NetCDF file path
        shapefile_path: Path to the shapefile (polygon geometry)
    """
    print("[DEBUG] Entered clip_netcdf_by_shapefile")
    print(f"[DEBUG] shapefile_path: {shapefile_path}")
    ds = xr.open_dataset(input_nc)
    # Detect coordinate variable names
    lat_name = 'latitude' if 'latitude' in ds.dims else ('lat' if 'lat' in ds.dims else None)
    lon_name = 'longitude' if 'longitude' in ds.dims else ('lon' if 'lon' in ds.dims else None)
    if lat_name is None or lon_name is None:
        print(f"[WARNING] Could not find standard latitude/longitude dimension names. Found dims: {ds.dims}")
    else:
        print(f"[DEBUG] NetCDF {lat_name} range: {ds[lat_name].min().values} ~ {ds[lat_name].max().values}")
        print(f"[DEBUG] NetCDF {lon_name} range: {ds[lon_name].min().values} ~ {ds[lon_name].max().values}")
        # Check if coordinates are 1D and regularly spaced
        if ds[lat_name].ndim != 1 or ds[lon_name].ndim != 1:
            print(f"[WARNING] NetCDF coordinates are not 1D. rioxarray.clip may not work as expected.")
        else:
            lat_diff = (ds[lat_name][1] - ds[lat_name][0]).values
            print(f"[DEBUG] {lat_name} step: {lat_diff}")
    ds = ds.rio.write_crs("EPSG:4326")
    gdf = gpd.read_file(shapefile_path)
    # Check CRS
    if gdf.crs is None:
        raise ValueError("Shapefile has no CRS. Please assign a coordinate reference system in QGIS.")
    if gdf.crs.to_string() != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    # Check geometry validity
    if not gdf.is_valid.all():
        print("[WARNING] Some geometries in the shapefile are invalid. Consider fixing them in QGIS.")
    # Merge all geometries into one MultiPolygon
    mask_geom = [gdf.unary_union]
    print(f"[DEBUG] Geometry type: {type(mask_geom[0])}, bounds: {mask_geom[0].bounds}")
    # Print bounds comparison
    if lat_name and lon_name:
        print(f"[DEBUG] NetCDF bounds: lat {ds[lat_name].min().values} ~ {ds[lat_name].max().values}, lon {ds[lon_name].min().values} ~ {ds[lon_name].max().values}")
    print(f"[DEBUG] Shapefile bounds: {mask_geom[0].bounds}")
    # Clip with all_touched=True
    clipped = ds.rio.clip(mask_geom, gdf.crs, drop=True, all_touched=True)
    print(f"[DEBUG] Clipped shape: {clipped.dims if hasattr(clipped, 'dims') else 'N/A'}")
    if hasattr(clipped, lat_name) and hasattr(clipped, lon_name):
        print(f"[DEBUG] Clipped NetCDF bounds: lat {clipped[lat_name].min().values} ~ {clipped[lat_name].max().values}, lon {clipped[lon_name].min().values} ~ {clipped[lon_name].max().values}")
    if clipped.dims.get(lat_name, 0) == 0 or clipped.dims.get(lon_name, 0) == 0:
        ds.close()
        clipped.close()
        raise ValueError("Clipped NetCDF is empty after shapefile mask. Please check your AOI.")
    clipped.to_netcdf(output_nc)
    ds.close()
    clipped.close()
