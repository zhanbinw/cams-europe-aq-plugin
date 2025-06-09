import xarray as xr

file_path = "D:/01POLIMI/03SEM2/CAMSProject/cams.eaq.vra.ENSa.nh3.l50.2022-01.nc"  #  full path
ds = xr.open_dataset(file_path)

print("📦 Data variables:", list(ds.data_vars))
print("📐 Dimensions:", ds.dims)

print("📊 Dimension structure for each variable:")
for var in ds.data_vars:
    print(f"  - {var}: {ds[var].dims}")