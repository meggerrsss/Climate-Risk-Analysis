#https://github.com/jwilgus/dist2coast/blob/main/dist_to_NA_coastline.py
# did not do what i wanted, scrapped
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points
from shapely.ops import unary_union
from haversine import haversine, Unit
import geoplot as gplt
import matplotlib.pyplot as plt

debug = True
# point coordinates for testing
lat = 35.08 # ~ ABQ locs
lon = -106.65
p0 = Point(lon,lat)

#--- Extract NA coastline geometry
file = r"C:\Users\CAMG038492\WSP O365\WDS-Digital Environment - Climatology Datasets - Climatology Datasets\Natural Earth Coastline Data\ne_110m_coastline\ne_110m_coastline.shp"
world = gpd.read_file(file)
for item in world.geometry: print(item)
exit()

#--- clip 10 m coastline to NA geometry
coastline = gpd.clip(gpd.read_file('ne_10m_coastline/ne_10m_coastline.shp')
                    ,NA_boundaries).to_crs('EPSG:4326')
coastline_union = unary_union(coastline.geometry)

#--- determine closest point along coastline
p1, p0 = nearest_points(coastline_union, p0)
print(list(p1.coords))
nearest_lon, nearest_lat = (p1.coords)[0]

#--- determine distance between points
dist = haversine([lat, lon],[nearest_lat, nearest_lon]) #points in lat,lon form


if debug:
    #--- Create geopandas dataframes for starting point and nearest coastline point
    df_start = pd.DataFrame({'Latitude': [lat],'Longitude': [lon]})
    start = gpd.GeoDataFrame(df_start,
            geometry=gpd.points_from_xy(df_start.Longitude, df_start.Latitude))
    df_nearest = pd.DataFrame({'Latitude': [nearest_lat],'Longitude': [nearest_lon]})
    nearest = gpd.GeoDataFrame(df_nearest,
              geometry=gpd.points_from_xy(df_nearest.Longitude, df_nearest.Latitude))

    #plot input point (red) and "closest point" (blue) on coastline
    ax = gplt.polyplot(gpd.GeoSeries(NA_boundaries), figsize=(8, 5))
    start.plot(ax = ax, color = 'red')
    nearest.plot(ax = ax, color = 'blue')
    plt.title('starting loc '+str(np.round(lat,2))+','+str(np.round(lon,2))+'  closest coast loc '+
               str(np.round(nearest_lat,2))+','+str(np.round(nearest_lon,2))+' --> '+str(np.round(dist,2))+' [km]')
    plt.show()
    plt.close()