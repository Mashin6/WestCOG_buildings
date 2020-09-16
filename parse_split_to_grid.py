# Splitting westCOG area into square grid for tiled import
import re
import geopandas as gpd
import pandas as pd
from shapely import speedups
import numpy as np
from shapely.geometry import Polygon


speedups.enable()

# Load westCOG area as polygon tagged as building=yes
poly = gpd.read_file("westCOG-polygon-extended.geojson")
poly = poly.loc[poly['building'] == "yes"]


 # Get BBOX of westCOG polygon
xmin,ymin,xmax,ymax =  poly.total_bounds

# Set width and height
#width = 2000
#height = 1000

# Get number of rows and columns
#rows = int(np.ceil((ymax-ymin) / height))
#cols = int(np.ceil((xmax-xmin) / width))

# We want grid of 22x41 squares
rows = 41
cols = 23
width = ((xmax-xmin) / cols)
height = ((ymax-ymin) / rows)

# Set square sides
XleftOrigin = xmin
XrightOrigin = xmin + width
YtopOrigin = ymax
YbottomOrigin = ymax - height

# Make sqaures
polygons = []
for i in range(cols):
    Ytop = YtopOrigin
    Ybottom = YbottomOrigin
    for j in range(rows):
        polygons.append(Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)])) 
        Ytop = Ytop - height
        Ybottom = Ybottom - height
    XleftOrigin = XleftOrigin + width
    XrightOrigin = XrightOrigin + width

grid = gpd.GeoDataFrame({'geometry':polygons})
grid.crs = "EPSG:4326"


# Cut grid sqares with westCOG polygon
#gpd.overlay(grid, poly, how = 'intersection')


# Get all squares that overlap with westCOG polygon without cutting out westCOG shape
intersect = gpd.GeoDataFrame()
cutIntersect = gpd.overlay(grid, poly, how = 'intersection')
for i in range(0, len(cutIntersect)):
    xmin,ymin,xmax,ymax =  cutIntersect[i:i+1].centroid.total_bounds
    intersect = pd.concat([intersect, grid.cx[xmin:xmax, ymin:ymax]]).pipe(gpd.GeoDataFrame)


intersect = intersect.reset_index().drop(columns=['index'])

# Load westCOG high population areas 
hiPop = gpd.read_file("westCOG-hiPopulatioDensity.geojson")


# Find squares that overlap with high population areas
intersect['isDense'] = False
for i in range(0, len(intersect)):
    for j in range(0, len(hiPop)):
        isDense = intersect.iloc[i]['geometry'].intersects(hiPop.iloc[j]['geometry'])
        if isDense == True:
            intersect.loc[i:i, 'isDense'] = True
            continue

# Split marked squares into 4 smaller squares
toSplit = intersect.loc[intersect['isDense'] == True]['geometry'].tolist()

splitPolygons = []
for i in range(0, len(toSplit)):
    coords = toSplit[i].exterior.coords.xy
    coordW = list(set(coords[0]))
    coordH = list(set(coords[1]))
    coordW.insert(1, (coordW[0] + coordW[1]) / 2 )
    coordH.insert(1, (coordH[0] + coordH[1]) / 2 )
    splitPolygons.append(Polygon([(coordW[0], coordH[0]), (coordW[0], coordH[1]), (coordW[1], coordH[1]), (coordW[1], coordH[0])])) 
    splitPolygons.append(Polygon([(coordW[1], coordH[0]), (coordW[1], coordH[1]), (coordW[2], coordH[1]), (coordW[2], coordH[0])])) 
    splitPolygons.append(Polygon([(coordW[0], coordH[1]), (coordW[0], coordH[2]), (coordW[1], coordH[2]), (coordW[1], coordH[1])]))
    splitPolygons.append(Polygon([(coordW[1], coordH[1]), (coordW[1], coordH[2]), (coordW[2], coordH[2]), (coordW[2], coordH[1])]))


splitPolygons = gpd.GeoDataFrame({'geometry': splitPolygons})

# Merge nonsplitted with splitted squares
complete = pd.concat([intersect.loc[intersect['isDense'] != True], splitPolygons]).pipe(gpd.GeoDataFrame)



# Remove squares that becacme outside od WestCOG
intersect2 = gpd.GeoDataFrame()
cutIntersect2 = gpd.overlay(complete, poly, how = 'intersection')
for i in range(1, len(cutIntersect2)):
    xmin,ymin,xmax,ymax =  cutIntersect2[i-1:i].centroid.total_bounds
    intersect2 = pd.concat([intersect2, complete.cx[xmin:xmax, ymin:ymax]]).pipe(gpd.GeoDataFrame)


Final = intersect2.reset_index().drop(columns=['index', 'isDense'])

# Create tags for URL
for i in range(0, len(Final)):
    Final.loc[i:i, 'name'] = "Fragment_" + str(i+1)
    Final.loc[i:i, 'URL'] = "https://lepiller.eu/files/ct-import/westcog/" + Final.loc[i]['name'] + ".geojson"


# Save
Final.to_file('westCOG-grid.geojson', driver='GeoJSON')



### Split data
## Split Buildings data into according to computed areas
buildings = gpd.read_file("Buildings-Address-combined.geojson")

drop = []
for i in range(0, len(Final)):
    xmin, ymin, xmax, ymax = Final[i:i+1].total_bounds
    part = buildings.cx[xmin:xmax, ymin:ymax]
    if len(part) == 0:
        print("part row" + str(i) +  "is empty")
        drop.append(i)
        continue
    path = 'Address/Grid/' + Final['name'].iloc[i] + '.geojson'
    part.to_file(path, driver='GeoJSON')


# Remove squares that were empty
Final.drop(drop, inplace=True)
Final.to_file('westCOG-grid-final.geojson', driver='GeoJSON')







## Plotting of intermediate steps
######
pd.concat([grid, poly]).pipe(gpd.GeoDataFrame).exterior.plot()
pd.concat([cutIntersect, poly]).pipe(gpd.GeoDataFrame).exterior.plot()
pd.concat([intersect, poly]).pipe(gpd.GeoDataFrame).exterior.plot()
pd.concat([hiPop, poly]).pipe(gpd.GeoDataFrame).exterior.plot()
pd.concat([intersect.loc[intersect['isDense'] == True], poly, hiPop]).pipe(gpd.GeoDataFrame).exterior.plot()
pd.concat([complete, poly, hiPop]).pipe(gpd.GeoDataFrame).exterior.plot()
pd.concat([Final, poly, hiPop]).pipe(gpd.GeoDataFrame).exterior.plot()
plt.show()

shapely.ops.split(geom, splitter)






