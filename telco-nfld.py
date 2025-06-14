import dash
from dash import dcc, html
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import os

# --- Load GeoJSON Data ---
file_path_points = r"telco-nfld-dash/towers.geojson"
file_path_buffers = r"telco-nfld-dash/buffers.geojson"

gdf_points = gpd.read_file(file_path_points)
gdf_buffers = gpd.read_file(file_path_buffers)

# --- Create a Folium Map ---
m = folium.Map(location=[48.67, -56.35], zoom_start=8)

# Add GeoJSON points
folium.GeoJson(gdf_points, name="Points").add_to(m)

# Add GeoJSON buffers with styling
folium.GeoJson(gdf_buffers, name="Buffers", style_function=lambda x: {
    "fillColor": "lightblue",
    "color": "black",
    "weight": 2,
    "fillOpacity": 0.2
}).add_to(m)

# --- Save map to Dash assets folder ---
assets_folder = "assets"
os.makedirs(assets_folder, exist_ok=True)  # Ensure assets folder exists
map_path = os.path.join(assets_folder, "map.html")
m.save(map_path)

# --- Dash App ---
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Cell Towers and Service Areas in Newfoundland"),
    html.Iframe(src=app.get_asset_url("map.html"), width="100%", height="600px")  # Correct way to embed Folium map
])

if __name__ == "__main__":
    app.run(debug=True)
