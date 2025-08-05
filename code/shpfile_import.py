import geopandas as gpd

# Path to your shapefile (.shp)
shapefile_path = "G:/My Drive/DVS/Mentorship 2025 Summer Cohort/Humanitarian Aid Tool/geo/Sudan/sdn_adm_cbs_nic_ssa_20200831_shp.zip"

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# Show basic info
print(gdf.info())
print(gdf.head())