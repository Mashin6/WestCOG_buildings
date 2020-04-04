import geopandas as gpd
import pandas as pd
from collections import OrderedDict 

buildings_shp = gpd.read_file('Buildings.shp')

buildings_shp = buildings_shp.to_crs("EPSG:4326")

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


# Find all building parts that form one building (touch each other)
building = []
i = 0

# Cycle through all building parts
for part_id in range(0, len(buildings_shp)):
	# Skip if building part was already found, else create new building object
	if part_id in sum(building, []): continue
	else: building.append([part_id])

  
	for select_part_id in building[i]:
		neighbors = buildings_shp.geometry.touches(buildings_shp.geometry[select_part_id])
		ind = buildings_shp.loc[list(neighbors)].index.tolist()

		# Add parts to building object; This will force check of these new part for additional attached parts
		building[i].extend(ind)

		# Remove duplicates while preserving order of values using OrderDict
		building[i] = list(OrderedDict.fromkeys(building[i]))

	i += 1


# Get outline of combined building parts
for b in building:
	if len(b) == 1:
		buildings_shp.loc[b[0], 'building'] = 'yes'
		buildings_shp.loc[b[0], 'FCODE'] = 'none'

	else:
		outline = gpd.GeoDataFrame({'geometry': buildings_shp.iloc[b, ].unary_union, 'building': ['yes']})
		buildings_shp = pd.concat([buildings_shp, outline]).pipe(gpd.GeoDataFrame)


# Re-label building parts
buildings_shp.loc[buildings_shp['FCODE'] != 'none', 'building:part'] = 'yes'
buildings_shp = buildings_shp.drop(columns=['FCODE'])
# Fix: remove negative height data
buildings_shp = buildings_shp.drop[ buildings_shp[buildings_shp['BLDGHEIGHT'] <= 0].index ]



# Save output to shape file
buildings_shp.to_file('Buildings-parsed.shp')
