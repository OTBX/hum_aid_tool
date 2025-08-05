import pandas as pd
import geopandas as gpd
import numpy as np

# Assign the flatfile path (csv) to a variable
in_flatfile = "G:/My Drive/DVS/Mentorship 2025 Summer Cohort/Humanitarian Aid Tool/data/in/flat/Sudan Indicators.csv"

# Assign the shapefile path to a variable
in_shapefile = "G:/My Drive/DVS/Mentorship 2025 Summer Cohort/Humanitarian Aid Tool/data/in/geo/sdn_adm_cbs_nic_ssa_20200831_shp.zip"

# Assign the output shapefile path a name and variable
output_shapefile_path = "G:/My Drive/DVS/Mentorship 2025 Summer Cohort/Humanitarian Aid Tool/data/out/geo/Sudan_Indicators_Merged.shp"

# --- Begin parsing the flatfile ---

# Read csv and load into dataframe
df = pd.read_csv(in_flatfile, encoding="ISO-8859-1")
print(f"\n--- Flatfile Successfully Imported From:\n{in_flatfile}")

# Print information to review dataframe before cleaning
print("\n\n--- DataFrame Info Before Cleaned ---")
print(df.info())

# Summary of missing values before clean
missing_summary_before = df.isnull().sum()
print("\n\n--- Missing DataFrame Values Summary Before Clean ---\n", missing_summary_before)

# Print first 5 records of dataframe and last 10 records
print("\n--- DataFrame Head (can be any number of records) ---\n")
print(df.head())
print("\n--- DataFrame Tail ---\n\n")
print(df.tail(10))

# Standardize column names to snake_case
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("+", "", regex=False)
              .str.replace("#", "", regex=False)
)

# Drop row 2
df = df.drop([0])

# Define columns to be dropped in one place
# Get the names of the first 6 columns
cols_to_drop_by_pos = df.columns[:6].tolist()

# Define other columns to drop by name
cols_to_drop_by_name = [
    "admin_level",
    "reference_period_start",
    "reference_period_end"
]

# Combine the lists and drop all unwanted columns in a single step
all_cols_to_drop = cols_to_drop_by_pos + cols_to_drop_by_name
df = df.drop(columns=all_cols_to_drop, errors='ignore')

# Now, drop rows with any remaining missing values
df.dropna(how='any', inplace=True)

# Print to review dataframe after cleaning
print("\n\n--- DataFrame Info After Cleaned ---")
print(df.info())

missing_summary_after = df.isnull().sum()
print("\n--- Missing Values Summary After Clean ---", missing_summary_after) 
print("\n--- DataFrame Head After Clean ---", df.head())


# --- Begin parsing the shapefile ---

# Read the shapefile and load into dataframe
gdf = gpd.read_file(in_shapefile, layer="sdn_admbnda_adm2_cbs_nic_ssa_20200831")
print(f"\n--- Shapefile Successfully Imported From:\n{in_shapefile}")

# Print information to review the geospatial dataframe
print("\n\n--- GeoDataFrame Info Before Cleaned ---")
print(gdf.info())

missing_summary_gdf = gdf.isnull().sum()
print("\n--- Missing Values Summary in GeoDataFrame before cleaning ---\n", missing_summary_gdf)

gdf.columns = (
    gdf.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("+", "", regex=False)
              .str.replace("#", "", regex=False)
)

# Define columns to be dropped in one place
# Get the names of the first 6 columns
cols_to_drop_by_pos = gdf.columns[5:19].tolist()

# Define other columns to drop by name
cols_to_drop_by_name = [
    "adm2_ar"
]

# Combine the lists and drop all unwanted columns in a single step
all_cols_to_drop = cols_to_drop_by_pos + cols_to_drop_by_name
gdf = gdf.drop(columns=all_cols_to_drop, errors='ignore')

# Print information to review the geospatial dataframe after cleaning
print("\n--- GeoDataFrame Info After Cleaned ---")
print(gdf.info())

missing_summary_gdf = gdf.isnull().sum()
print("\n--- Missing Values Summary in GeoDataFrame after cleaning ---", missing_summary_gdf)

# --- Merge the two DataFrames ---

print("\n--- Preparing to Merge ---")
print("Cleaned 'df' columns:", df.columns)
print("Cleaned 'gdf' columns:", gdf.columns)

# Perform the merge on the common key
merged_gdf = gdf.merge(
    df,
    how='left',              # Keep all the geographic shapes
    left_on='adm2_pcode',    # The key from the GeoDataFrame
    right_on='admin2_code'  # The key from the regular DataFrame
)

print("\n--- Merge Complete ---")
print("Cleaned 'gdf' columns:", merged_gdf.columns)

# Drop unnecessary fields
gdf = merged_gdf.drop(['admin2_code', 'admin2_name'], axis=1)
print(gdf.info())

# Rename Columns
gdf.columns = ['shp_len', 'shp_area', 'adm2', 'adm2_pcode', 'geometry', 'adm1', 'org_acr', 'org', 'org_desc', 'sec_code', 'sec']

# --- Inspect the Final Merged Data ---

# print("\n\n--- Final Merged GeoDataFrame Info ---")
print(gdf.info())
# print("\n--- Final Merged GeoDataFrame Head ---")
print(gdf.head())

# Export the GeoDataFrame to a shapefile.
# The driver 'ESRI Shapefile' is specified for clarity.
gdf.to_file(output_shapefile_path, driver='ESRI Shapefile')

print(f"\n--- Successfully exported the merged shapefile to:\n{output_shapefile_path}")