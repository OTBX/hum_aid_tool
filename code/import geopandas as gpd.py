import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import os

def clean_shapefile(input_path, output_path, target_crs=None):
    """
    Cleans a shapefile by:
    - Removing empty geometries
    - Fixing invalid geometries
    - Removing duplicates
    - Optionally reprojecting

    Parameters:
        input_path (str): Path to input .shp
        output_path (str): Path to cleaned .shp
        target_crs (str, optional): EPSG code or proj string for reprojection
    """
    # Load shapefile
    print(f"Loading {input_path}...")
    gdf = gpd.read_file(input_path)

    # Remove empty or null geometries
    gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull()]

    # Fix invalid geometries
    gdf["geometry"] = gdf["geometry"].buffer(0)

    # Remove duplicates
    gdf = gdf.drop_duplicates(subset="geometry")

    # Optional reprojection
    if target_crs:
        print(f"Reprojecting to {target_crs}...")
        gdf = gdf.to_crs(target_crs)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save cleaned shapefile
    gdf.to_file(output_path)
    print(f"Cleaned shapefile saved to {output_path}")

# Example usage
if __name__ == "__main__":
    input_shp = "data/input.shp"
    output_shp = "data/cleaned_output.shp"
    clean_shapefile(input_shp, output_shp, target_crs="EPSG:4326")
