import geopandas as gpd
import pandas as pd
from shapely import speedups

speedups.enable()

buildings_shp = gpd.read_file('Buildings.shp')

# Remove unwanted objects
buildings_shp = buildings_shp.drop(buildings_shp.query('FCODE == "Patio"').index)
buildings_shp = buildings_shp.drop(buildings_shp.query('FCODE == "Deck"').index)
buildings_shp = buildings_shp.drop(buildings_shp.query('FCODE == "House trailer"').index)
buildings_shp = buildings_shp.drop(buildings_shp.query('FCODE == "Tank"').index)

buildings_shp = buildings_shp.reset_index()

# Remove unwanted tags
buildings_shp = buildings_shp.drop(columns=['index', 'OBJECTID', 'NUMSTORIES', 'FEATURECOD', 'LASTUPDATE', 'LASTEDITOR', 'BLDG_TOPEL', 'Status', 'Shape_Leng', 'Shape_Area'])

# Rename values
buildings_shp = buildings_shp.rename(columns={"BLDGHEIGHT": "height", "BLDG_GNDEL": "ele"})

# Convert feet to meters
buildings_shp.loc[:, 'height'] = round(buildings_shp.loc[:, 'height']/3.281, 2)
buildings_shp.loc[:, 'ele'] = round(buildings_shp.loc[:, 'ele']/3.281, 2)

# Fix: remove negative height data
buildings_shp.loc[buildings_shp['height'] <= 0, 'height'] = None

## Create building outline around building parts
# Combine all touching shapes into union shape
buildings_u=gpd.GeoDataFrame(geometry=list(buildings_shp.unary_union))
# Tag as buildings
buildings_u.loc[:, 'building'] = 'yes'
# Merge with original dataset
buildings_shp = pd.concat([buildings_shp, buildings_u]).pipe(gpd.GeoDataFrame)

## Remove building outlines that consist of a sigle building part (duplicate objects)
# Find buildings that consist of one object; Mark rows at the beging for keeping (as building)
buildings_shp.loc[ buildings_shp.duplicated(subset='geometry', keep='last') , 'building'] = 'yes'
# Remove .unary_union objects that were created from single objects building; Located at the end of dataframe
buildings_shp = buildings_shp.drop_duplicates(subset='geometry', keep='first')

# Re-label buildings parts
buildings_shp.loc[buildings_shp['building'] != 'yes', 'building:part'] = 'yes'
buildings_shp = buildings_shp.drop(columns=['FCODE'])

# Set as WGS84 transform
buildings_shp.crs = "EPSG:4326"

# Save output to shape file
buildings_shp.to_file('Buildings-parsed.shp')
buildings_shp.to_file('Buildings-parsed.geojson', driver='GeoJSON')
