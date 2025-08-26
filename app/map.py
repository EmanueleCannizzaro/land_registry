
import zipfile
import geopandas as gpd
from pathlib import Path
# from shapely.geometry import shape
import tempfile
from typing import List


# Global variable to store current geodataframe
current_gdf = None


def extract_qpkg_data(file_path):
    """Extract geospatial data from QPKG or GPKG file"""
    global current_gdf
    
    # If it's a GPKG file, read directly
    if file_path.endswith('.gpkg'):
        try:
            gdf = gpd.read_file(file_path)
            current_gdf = gdf
            return gdf.to_json()
        except Exception:
            return None
    
    # If it's a QPKG file, try to extract and search for geospatial files
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract QPKG (it's essentially a ZIP file)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Look for common geospatial file formats
            temp_path = Path(temp_dir)
            geospatial_files = []
            
            for ext in ['*.shp', '*.geojson', '*.gpkg', '*.kml']:
                geospatial_files.extend(temp_path.rglob(ext))
            
            # Read the first found geospatial file
            if geospatial_files:
                gdf = gpd.read_file(geospatial_files[0])
                current_gdf = gdf
                return gdf.to_json()
    
    except (zipfile.BadZipFile, zipfile.LargeZipFile):
        # If QPKG is not a ZIP file, try to read it directly as a geospatial file
        try:
            gdf = gpd.read_file(file_path)
            current_gdf = gdf
            return gdf.to_json()
        except Exception:
            pass
    
    return None


def get_current_gdf():
    """Get the current GeoDataFrame"""
    return current_gdf


def find_adjacent_polygons(gdf: gpd.GeoDataFrame, selected_idx: int, touch_method: str = "touches") -> List[int]:
    """
    Find polygons adjacent to the selected polygon.
    
    Args:
        gdf: GeoDataFrame containing polygons
        selected_idx: Index of the selected polygon
        touch_method: Method to determine adjacency ('touches', 'intersects', 'overlaps')
    
    Returns:
        List of indices of adjacent polygons
    """
    print(f"Finding adjacent polygons: selected_idx={selected_idx}, method={touch_method}, gdf_len={len(gdf)}")
    
    if selected_idx >= len(gdf):
        print(f"Selected index {selected_idx} is out of bounds")
        return []
    
    selected_geom = gdf.iloc[selected_idx].geometry
    print(f"Selected geometry type: {selected_geom.geom_type}")
    adjacent_indices = []
    
    for idx, row in gdf.iterrows():
        if idx == selected_idx:
            continue
            
        try:
            # Check spatial relationship
            if touch_method == "touches":
                is_adjacent = selected_geom.touches(row.geometry)
            elif touch_method == "intersects":
                is_adjacent = selected_geom.intersects(row.geometry) and not selected_geom.within(row.geometry)
            elif touch_method == "overlaps":
                is_adjacent = selected_geom.overlaps(row.geometry)
            else:
                # Default to touches
                is_adjacent = selected_geom.touches(row.geometry)
            
            if is_adjacent:
                print(f"Found adjacent polygon at index {idx}")
                adjacent_indices.append(idx)
                
        except Exception as e:
            print(f"Error checking adjacency for polygon {idx}: {e}")
            continue
    
    print(f"Total adjacent polygons found: {len(adjacent_indices)}")
    return adjacent_indices
