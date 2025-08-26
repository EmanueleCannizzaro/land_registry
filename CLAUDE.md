# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a QPKG Map Viewer application that allows users to upload QPKG files (QGIS project packages) and visualize their geospatial data on an interactive web map. The application is built with FastAPI backend and Leaflet frontend.

## Architecture

The project has a simple structure:
- `app.py` - FastAPI application with endpoints for uploading QPKG files and serving the map interface
- `map/map.py` - Core geospatial data extraction logic using geopandas and zipfile
- `templates/map.html` - Frontend HTML with Leaflet.js for interactive mapping

## Key Dependencies

- **FastAPI** - Web framework for the API endpoints
- **folium** - Python library for generating Leaflet maps (used in one endpoint but not the main flow)
- **geopandas** - Geospatial data processing and format conversion
- **Leaflet.js** - Frontend mapping library (loaded from CDN)

## Development Commands

Since there are no package.json, requirements.txt, or other standard configuration files, this appears to be a minimal Python project. To run the application:

```bash
# Install dependencies manually
pip install fastapi geopandas folium

# Run the development server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /upload-qpkg/` - Upload QPKG file and extract geospatial data as GeoJSON
- `GET /map/` - Serve the interactive map HTML page  
- `POST /generate-map/` - Generate map HTML from QPKG (incomplete implementation in app.py:50-81)

## Data Flow

1. User uploads QPKG file via web interface
2. Backend extracts ZIP contents and searches for geospatial files (.shp, .geojson, .gpkg, .kml)
3. Uses geopandas to read first found geospatial file and convert to GeoJSON
4. Frontend receives GeoJSON and renders on Leaflet map with popup attributes

## Important Notes

- QPKG files are treated as ZIP archives
- Static files served from `static/` directory (note: inconsistent paths between mount and file reading)
- Temporary files created during processing are cleaned up automatically
- The application expects geospatial data within the QPKG structure