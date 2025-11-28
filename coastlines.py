import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, MultiLineString, LineString
import shapely
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import geodesic
from math import radians, sin, cos
import os
import functools
from tqdm import tqdm

# locations to find
testsites = pd.read_csv(r"C:\Users\CAMG038492\Code\Climatology\archive\locations.csv")
#sites = pd.read_csv(r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Full Points CSV\minimalpoints.csv")
sitesfolder = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Point CSVs\4326 with elevation"
#sites = pd.read_csv(r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Point CSVs\4326\Capacitors.csv")
sitesfolder = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Underground"

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
@functools.lru_cache(maxsize=1000)
def densify_linestring(linestring, interval):
    if interval == '':
        return list(linestring.coords)
    else:
        length = linestring.length
        distances = np.arange(0, length, interval)
        points = [linestring.interpolate(distance) for distance in distances]
        numpoints = [(t.x,t.y) for t in points]
        s = linestring.interpolate(length)
        interpolated = s.x,s.y
        numpoints.append(interpolated)
        return numpoints


def build_tree(points_of_interest=[], interpolate='', max_distance=0):
    # create database of coastline linestring verticies
    points = []
    geoms = []
    if len(points_of_interest) > 0:
        for geom in tqdm(coastline.geometry, "finding geometry"):
            for p in points_of_interest:
                d = geom.distance(p)
                if d > max_distance:
                    break
                if d <1:
                    geoms.append(geom)
                    break
    else:
        geoms = coastline.geometry

    for geom in tqdm(geoms, desc = "Building Tree:"):
        if geom.geom_type == 'Point':
            points.extend(geom.coords[0])
        elif geom.geom_type == 'LineString':
            points.extend(densify_linestring(geom, interpolate))
            #points.extend(list(geom.coords))
        elif geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                points.extend(densify_linestring(line, interpolate))
                #points.extend(list(line.coords))

    # create tree of coastlines
    coords = np.array(points)
    tree = cKDTree(coords)
    return coords, tree

coords, tree = build_tree()

precise = False

if create_checkpoint:=True:
    coordspd = pd.DataFrame(coords)
    coordspd.to_csv(os.path.join(outputfolder, "coast-points-checkpoint.csv"))
    print(f"linestrings exported")

# finding the distance to the nearest coastline, in km
def nearest(lat, lon, tree, coords, crs = 'ESRI:53032'):
    # convert query point to a Point
    query_point = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326')
    query_point_proj = query_point.to_crs(crs)
    x, y = query_point_proj.geometry[0].x, query_point_proj.geometry[0].y

    # do the tree
    if precise:
        i, idxs = tree.query([x, y], k=10)
        candidates = [Point(*coords[idx]) for idx in idxs]
        c, near_tree = build_tree(candidates, 1, i[-1]*2)
        i, idx = near_tree.query([x, y])
        nearestpt = c[idx]
    else:
        _, nearestpt = tree.query([x,y])
        nearestpt = coords[nearestpt]

    # convert point to a Point again
    nearestpt_crs = gpd.GeoSeries([Point(nearestpt[0], nearestpt[1])], crs=crs)
    nearestpt_4326 = nearestpt_crs.to_crs('EPSG:4326')
    outx, outy = nearestpt_4326.geometry[0].x, nearestpt_4326.geometry[0].y

    #Convert nearest candidate to Point
    if precise:
        nearest_candidate_crs = gpd.GeoSeries([candidates[0]], crs=crs)
        nearest_candidate_4326 = nearest_candidate_crs.to_crs('EPSG:4326').geometry[0]


    # return distance
    outd = {}
    outd['distance'] = geodesic((lat, lon), (outy, outx)).kilometers
    outd['position'] = [outy, outx]
    if precise: outd['candidate_pos'] = [nearest_candidate_4326.y,nearest_candidate_4326.x]
    return outd


def v_nearest(row, which:str):
    if which == "dist":
        return nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)['distance']
    if which == "both":
        return nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)['position']
    if which == "lat":
        return nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)['position'][0]
    if which == "lon":
        return nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)['position'][1]
    if which == "candidate_lat" and precise:
        return nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)['candidate_pos'][0]
    if which == "candidate_lon" and precise:
        return nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)['candidate_pos'][1]
    if which == "attempt" and precise:
        n = nearest(lat = row.Y, lon = row.X, tree = tree, coords = coords)
        return [n['position'][0], n["position"][1], n['candidate_pos'][0], n["candidate_pos"][1]]

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
        sites = sites.sample(n=10)
        sites.to_csv(os.path.join(outputfolder, "sample-sites.csv"))

    sites["Nearest coast (km)"] = sites.apply(v_nearest, which="dist", axis = 1)
    sites["Nearest coast (lat,lon)"] = sites.apply(v_nearest, which="both", axis = 1)
    sites["Nearest coast (lat)"] = sites.apply(v_nearest, which="lat", axis = 1)
    sites["Nearest coast (lon)"] = sites.apply(v_nearest, which="lon", axis = 1)
    # sites["Nearest candidate (lat)"] = sites.apply(v_nearest, which="candidate_lat", axis = 1)
    # sites["Nearest candidate (lon)"] = sites.apply(v_nearest, which="candidate_lon", axis = 1)
    #sites["Coastline coverage at 50km (%)"] = sites.apply(v_angles, km = 50, axis = 1)
    #sites['attempt'] = sites.apply(v_nearest, which="attempt", axis=1)
    #sites[["Nearest coast (lat)", "Nearest coast (lon)", "Nearest candidate (lat)", "Nearest candidate (lon)"]] = pd.DataFrame(sites.attempt.tolist(), index=sites.index)

    # exporting
    if export := True:
        if create_sample:
            sites[["Nearest coast (lat)", "Nearest coast (lon)", "Nearest candidate (lat)", "Nearest candidate (lon)"]].to_csv(os.path.join(outputfolder, "sample-nearest-coast.csv"))
            exit()
        else:
            newfolder = r"C:\Users\CAMG038492\OneDrive - WSP O365\Documents\Climate Data\NF Power GIS\Coastline CSVs\Exports"
            sites.to_csv(os.path.join(newfolder, name))
            print(f"coastline file created for {name}")



# printing options
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 10)
print(sites.head())
