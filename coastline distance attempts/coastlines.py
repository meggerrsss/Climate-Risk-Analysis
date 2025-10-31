import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import geodesic
from math import radians, sin, cos

sites = pd.read_csv(r"C:\Users\CAMG038492\Code\Climatology\archive\locations.csv")
file = r"C:\Users\CAMG038492\WSP O365\WDS-Digital Environment - Climatology Datasets - Climatology Datasets\Natural Earth Coastline Data\ne_10m_coastline\ne_10m_coastline.shp"
coastline = gpd.read_file(file)

points = []
for geom in coastline.geometry:
    if geom.geom_type == 'LineString':
        points.extend(list(geom.coords))
    elif geom.geom_type == 'MultiLineString':
        for line in geom:
            points.extend(list(line.coords))

coords = np.array(points)
tree = cKDTree(coords)

# finding the distance to the nearest coastline, in km
def nearestdist(lat, lon, tree, coords):
    i, idx = tree.query([lon, lat])
    nearestpt = coords[idx]
    return geodesic((lat, lon), (nearestpt[1], nearestpt[0])).kilometers

def v_nearestdist(row):
    return nearestdist(lat = row.Y, lon = row.X, tree = tree, coords = coords)

# finding the location of the nearest coastline, in lat,lon
def nearestloc(lat, lon, tree, coords):
    i, idx = tree.query([lon, lat])
    nearestpt = coords[idx]
    return [nearestpt[1],nearestpt[0]]

def v_nearestloc(row, which:str):
    if which == "both":
        return nearestloc(lat = row.Y, lon = row.X, tree = tree, coords = coords)
    if which == "lat":
        return nearestloc(lat = row.Y, lon = row.X, tree = tree, coords = coords)[0]
    if which == "lon":
        return nearestloc(lat = row.Y, lon = row.X, tree = tree, coords = coords)[1]

# finding the angular coverage of coastline a specific distance away
# exactly at 50km, would need to test for within 50km probably
# looking for LINES or looking for things past the line
def angles(lat, lon, maxkm = 50, step = 1, tree = None, coords = None):
    steps = int(360 / step)
    count = 0

    for angle in range(0, 360, step):
        rad = radians(angle)

        # mystery math i'm trusting bing on this one
        end_lat = lat + (maxkm / 111) * cos(rad)
        end_lon = lon + (maxkm / (111 * cos(radians(lat)))) * sin(rad)

        i, idx = tree.query([end_lon, end_lat])
        spot = coords[idx]

        dist = geodesic((lat, lon), (spot[1], spot[0])).kilometers

        if dist <= maxkm:
            count += 1

    return (count / steps) * 100

def v_angles(row, km):
    return angles(lat = row.Y, lon = row.X, maxkm = km, tree = tree, coords = coords)

sites["Nearest coast (km)"] = sites.apply(v_nearestdist, axis = 1)
sites["Nearest coast (lat,lon)"] = sites.apply(v_nearestloc, which="both", axis = 1)
sites["Nearest coast (lat)"] = sites.apply(v_nearestloc, which="lat", axis = 1)
sites["Nearest coast (lon)"] = sites.apply(v_nearestloc, which="lon", axis = 1)
sites["Coastline coverage at 50km (%)"] = sites.apply(v_angles, km = 50, axis = 1)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)
print(sites)
