import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, MultiLineString, LineString
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import geodesic
from math import radians, sin, cos
import os
from tqdm import tqdm

# locations to find
testsites = pd.read_csv(r"C:\Users\CAMG038492\Code\Climatology\archive\locations.csv")
#sites = pd.read_csv(r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Full Points CSV\minimalpoints.csv")
sitesfolder = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Point CSVs\4326"
#sites = pd.read_csv(r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Point CSVs\4326\Capacitors.csv")

# coastline data
ne_file = r"C:\Users\CAMG038492\WSP O365\WDS-Digital Environment - Climatology Datasets - Climatology Datasets\Natural Earth Coastline Data\ne_10m_coastline\ne_10m_coastline.shp"
nf_file = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\testing coastline shapefile conversion\erosion.shp"
nf_file_azi = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\testing coastline shapefile conversion\erosion-azi.shp"
ne_coastline = gpd.read_file(ne_file)
nf_coastline = gpd.read_file(nf_file)
nf_azi_coastline = gpd.read_file(nf_file_azi) # converted with qgis
nf_azi2_coastline = nf_coastline.to_crs('ESRI:53032')  # converted with shapely
coastline = nf_azi2_coastline
outputfolder = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Coastline CSVs"

# open list of csvs into a dictionary
def open_csvs(folder):
    d = {}
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            d[file] = pd.read_csv(os.path.join(folder,file))
    return d

# interpolate linestrings to be denser, so that locations on midpoints of string can be valid "closests"
def densify_linestring(linestring, interval):
    if interval == '':
        return list(linestring.coords)
    else:
        length = linestring.length
        distances = np.arange(0, length, interval)
        points = [linestring.interpolate(distance) for distance in distances]
        points.append(linestring.interpolate(length))
    return points

# create database of coastline linestring verticies
points = []
for geom in tqdm(coastline.geometry, desc = "Building Tree: "):
    if geom.geom_type == 'Point':
        points.extend(geom.coords[0])
    elif geom.geom_type == 'LineString':
        points.extend(densify_linestring(geom, ''))
        #points.extend(list(geom.coords))
    elif geom.geom_type == 'MultiLineString':
        for line in geom.geoms:
            points.extend(densify_linestring(line, ''))
            #points.extend(list(line.coords))


# create tree of coastlines
coords = np.array(points)
tree = cKDTree(coords)

# finding the distance to the nearest coastline, in km
def nearestdist(lat, lon, tree, coords, crs = 'ESRI:53032'):
    # convert query point to a Point
    query_point = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326')
    query_point_proj = query_point.to_crs(crs)
    x, y = query_point_proj.geometry[0].x, query_point_proj.geometry[0].y

    # do the tree
    i, idx = tree.query([x, y])
    nearestpt = coords[idx]

    # convert point to a Point again
    nearestpt_crs = gpd.GeoSeries([Point(nearestpt[0], nearestpt[1])], crs=crs)
    nearestpt_4326 = nearestpt_crs.to_crs('EPSG:4326')
    outx, outy = nearestpt_4326.geometry[0].x, nearestpt_4326.geometry[0].y

    # return distance
    return geodesic((lat, lon), (outy, outx)).kilometers

def v_nearestdist(row):
    return nearestdist(lat = row.Y, lon = row.X, tree = tree, coords = coords)

# finding the location of the nearest coastline, in lat,lon
def nearestloc(lat, lon, tree, coords, crs = 'ESRI:53032'):
    # convert query point to a Point
    query_point = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326')
    query_point_proj = query_point.to_crs(crs)
    x, y = query_point_proj.geometry[0].x, query_point_proj.geometry[0].y

    # do the tree
    i, idx = tree.query([x, y])
    nearestpt = coords[idx]

    # convert point to a Point again
    nearestpt_crs = gpd.GeoSeries([Point(nearestpt[0], nearestpt[1])], crs=crs)
    nearestpt_4326 = nearestpt_crs.to_crs('EPSG:4326')
    outx, outy = nearestpt_4326.geometry[0].x, nearestpt_4326.geometry[0].y

    # return locations
    return [outy, outx]

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

# run across all files
for site,df in open_csvs(sitesfolder).items():
    name = site
    sites = df

    # take a small test selection of sites
    create_sample = False
    if create_sample:
        sites = sites.sample(n=30, random_state=42)
        sites.to_csv(os.path.join(outputfolder, "sample-sites.csv"))

    sites["Nearest coast (km)"] = sites.apply(v_nearestdist, axis = 1)
    sites["Nearest coast (lat,lon)"] = sites.apply(v_nearestloc, which="both", axis = 1)
    sites["Nearest coast (lat)"] = sites.apply(v_nearestloc, which="lat", axis = 1)
    sites["Nearest coast (lon)"] = sites.apply(v_nearestloc, which="lon", axis = 1)
    #sites["Coastline coverage at 50km (%)"] = sites.apply(v_angles, km = 50, axis = 1)

    # exporting
    if export := True:
        if create_sample:
            sites[["Nearest coast (lat)", "Nearest coast (lon)"]].to_csv(os.path.join(outputfolder, "sample-nearest-coast.csv"))
            exit()
        else:
            newfolder = sitesfolder.replace(r"Point CSVs\4326", r"Coastline CSVs\Exports")
            sites.to_csv(os.path.join(newfolder, name))
            print(f"coastline file created for {name}")



# printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)
print(sites)
