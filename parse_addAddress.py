import re
import geopandas as gpd
import pandas as pd
from shapely import speedups

speedups.enable()

# to Expand street suffix
def expandSuffix(text):
    suffixDb = {
    "Av": "Avenue",
    "Ave": "Avenue",
    "Apts": "Apartment",
    "Blvd": "Boulevard",
    "Bl": "Boulevard",
    "Blf": "Bluff",
    "Brg": "Bridge",
    "Brk": "Brook",
    "Cir": "Circle",
    "Ci": "Circle",
    "Cl": "Close",
    "Cmn": "Common",
    "Cmns": "Commons",
    "Conn": "Connector",
    "Cres": "Crescent",
    "Crt": "Court",
    "Ct": "Court",
    "Cr": "Crossing",
    "Ctr": "Center",
    "Crst": "Crest",
    "Cv": "Cove",
    "Prof": "Professional",
    "Pro": "Professional",
    "Div": "Diversion",
    "Dr": "Drive",
    "Dl": "Dale",
    "D": "Drive",
    "Drs": "Drive South",
    "E": "East",
    "Fld": "Field",
    "Gr": "Grove",
    "Grv": "Grove",
    "Gln": "Glen",
    "Grn": "Green",
    "Hbr": "Harbor",
    "Hwy": "Highway",
    "Hl": "Hill",
    "Hlw": "Hollow",
    "Holw": "Hollow",
    "Hts": "Heights",
    "Hgts": "Heights",
    "Lane": "Lane",
    "La": "Lane",
    "Ln": "Lane",
    "Lndg": "Landing",
    "Mnr": "Manor",
    "Mtn": "Mountain",
    "Mt": "Mountain",
    "Ml": "Mill",
    "Mdws": "Meadows",
    "Tl": "Trail",
    "N": "North",
    "No": "North",
    "Orch": "Orchard",
    "Pkwy": "Parkway",
    "Pl": "Place",
    "Plz": "Plaza",
    "Pt": "Point",
    "Rd": "Road",
    "Rwy": "Railway",
    "S": "South",
    "So": "South",
    "Shr": "Shore",
    "Shrs": "Shores",
    "Spg": "Springs",
    "Spgs": "Springs",
    "Sq": "Square",
    "St": "Street",
    "Sw": "South West",
    "Trl": "Trail",
    "W": "West",
    "Is": "Island",
    "Wy": "Way",
    "Tr": "Terrace",
    "Te": "Terrace",
    "Ter": "Terrace",
    "Terr": "Terrace",
    "Pk": "Park",
    "Sq": "Square",
    "Pz": "Plaza",
    "Tpke": "Turnpike",
    "Wy": "Way",
    "Ex": "Extension",
    "Ext": "Extension",
    "Ext.": "Extension",
    "Knl": "Knoll",
    "Knls": "Knolls",
    "Lk": "Lake",
    "Rdg": "Ridge",
    "Roughrd": "Rough Road",
    "Vis": "Vista",
    "Vlg": "Village"
    }
    for k, v in suffixDb.items():
        if text == None:
            break
        if text == "DR MARTIN LUTHER KING JR":
            text = text.title()
            break
        text = ' '.join(v if word == k else word for word in text.title().split())
    return(text)
    

# Parse LOCATION tag
def parseLocation(text):
    out = [None] * 4
    #[0] : House number
    #[1] : Unit
    #[2] : Street
    #[3] : City
    # Catch irregular exceptions
    if text == None:
        return(out)
    if text == "N.Y.N.H.&H.R.R.":
        return(out)
    elif text == "Fairview Dr 39-2 Bldg 2":
        out[0] = "39-2"
        out[1] = "2"
        out[2] = "Fairview Drive"
        return(out)
    elif text == "SHELTER ROCK ROAD F9":
        out[1] = "F9"
        out[2] = "Shelter Rock Road"
        return(out)
    elif text == "BUMPY LN WSPT":
        out[2] = "Bunmpy Lane"
        out[3] = "Wesrport"
        return(out)
    elif text == "COVLEE DR - WSPT":
        out[2] = "Covlee Drive"
        out[3] = "Wesrport"
        return(out)
    elif text == "DANBURY RD-WILTON":
        out[2] = "Danbury Road"
        out[3] = "Wilton"
        return(out)
    elif text == "SILVERMINE RD-NEW CANAAN":
        out[2] = "Silvermine Road"
        out[3] = "New Canaan"
        return(out)
    elif text == "Haddad Dr 12":
        out[0] = "12"
        out[2] = "Haddad Drive"
        return(out)
    elif text == "Kohanza St 5-99":
        out[0] = "5-99"
        out[2] = "Kohanza Street"
        return(out)
    elif text == "Newtown":
        out[3] = "Newtown"
        return(out)
    elif text == "0017 SHELLEY ROAD  (BETHEL)":
        out[1] = "17"
        out[2] = "Shelley Road"
        out[3] = "Bethel"
        return(out)
    elif text == "1 Fairfield Av G1":
        out[0] = "1"
        out[1] = "G1"
        out[2] = "Fairfield Avenue"
        return(out)
    elif text == "SHELTER ROCK RD F17":
        out[1] = "F17"
        out[2] = "Shelter Rock Road"
        return(out)
    elif text == "OLD POST ROAD NO 2":
        out[2] = "Old Post Road No 2"
        return(out)
    elif text == "22A Virginia Av 2":
        out[0] = "22A"
        out[1] = "2"
        out[2] = "Virginia Avenue"
        return(out)
    elif text == "OLD POST ROAD NO 3":
        out[2] = "Old Post Road No 3"
        return(out)
    elif text == "D Foster St 3":
        out[0] = "3"
        out[2] = "Foster Street"
        out[3] = "Danbury"
        return(out)
    elif text == "SOSSE CT (LEWIS WAY)":
        out[2] = "Sosse Court"
        return(out)
    elif text == "0001 TOTEM TRAIL  SEE NOTE":
        out[0] = "1"
        out[2] = "Totem Trail"
        return(out)
    elif text == "RIVERSIDE A  I-84":
        out[2] = "Riverside A"
        return(out)
    elif text == "LITTLEFIELD RD (RECA)":
        out[2] = "Littlefield Road"
        return(out)
    elif text == "MAIN ST (GREEN)":
        out[2] = "Main Street"
        return(out)
    elif text == "LITTLEFIELD RD (WELL)":
        out[2] = "Littlefield Road"
        return(out)
    elif text == "LITTLEFIELD RD (WELL)":
        out[2] = "Littlefield Road"
        return(out)
    elif text == "MAPLE AVE REAR F12 F":
        out[2] = "Maple Avenue"
        return(out)
    elif text == "1 Raymond Pl A":
        out[0] = "1"
        out[1] = "A"
        out[2] = "Raymond Place"
        return(out)
    elif text == "OAK RIDGE+EVERGRN OP":
        return(out)
    elif text == "Passway No 3":
        out[2] = "Passway No 3"
        return(out)
    elif text == "WISHING WELL LN  #7":
        out[0] = "7"
        out[2] = "Wishing Well Lane"
        return(out)
    elif text == "9  WISHING WELL LN  #9":
        out[0] = "9"
        out[2] = "Wishing Well Lane"
        return(out)
    elif text == "5  WISHING WELL LN  #5":
        out[0] = "5"
        out[2] = "Wishing Well Lane"
        return(out)
    elif text == "Quarry Road(Turkey Plain":
        out[2] = "Quarry Road"
        return(out)
    x = text.title().split()
    # House number
    ## For numbers 000023 --> 23
    if x[0].isnumeric():
        out[0] = str(int(x[0]))
        x.pop(0)
    ## For hyphen numbers 1-24
    elif (x[0].find('-') != -1):
        out[0] = x[0]
        x.pop(0)
    ## For number-letter conbinations 0002A --> 2A
    elif any(map(str.isdigit, x[0])):
        y = re.split(r'(\d+)', x[0])
        y[1] = str(int(y[1]))
        out[0] = ''.join(y)
        x.pop(0)
    #Unit/apartment number
    if x[-1].isnumeric():
        out[1] = str(int(x[-1]))
        x.pop(-1)
    elif (x[-1].find('-') != -1):
        out[1] = x[-1]
        x.pop(-1)
    out[2] = ' '.join(x)     
    return(out)

# Fix subadress numbers
def fixSubaddress(text):
    if text == None:
            return(text)
    text = text.replace('(','')
    text = text.replace(')','')
    text = text.replace('UNIT','')
    text = text.replace('UN ','')
    text = text.replace('UN','')
    text = text.replace('CONDO','')
    text = text.replace('#','')
    if text in {'-MAIN HS/116-TENA', '-CHURCH/4-CHAPEL', '-HS/95-CABIN', '-RES/4-TENANT HS'}:
        text = None
    return(text)

# Read data    
address = gpd.read_file("Connecticut_Buildings_with_Addresses_experimental.shp")

# Subset for westCOG towns
# N0te: Weston, Ridgefield, New Fairfield are not part of dataset

address = address.loc[ address['TOWN_NO'].isin([9, 16, 18, 34, 35, 57, 90, 96, 97, 103, 117, 127, 135, 158, 161]) ]
address = address.reset_index()

address = address.drop(columns=['OBJECTID', 'FID_Parcel', 'Join_Count', 'TARGET_FID', 'MBL', 'PIN', 'ACRES', 'SeparatorE', 'StreetNa_7', 'Subaddre_2',
  'Subaddre_5', 'Subaddre_8', 'Subaddre_9', 'Subaddre10', 'Subaddre11', 'Subaddre12', 'Subaddre13', 'Subaddre14', 'Subaddre15', 'Subaddre16', 
  'Subaddre17', 'StateName', 'ESN', 'AddressID', 'RelatedAdd', 'AddressRel', 'AddressPar', 'AddressP_1', 'AddressXCo', 'AddressYCo', 'AddressEle',
  'AddressCla', 'AddressLif', 'OfficialSt', 'AddressAno', 'AddressSta', 'AddressEnd', 'AddressDir', 'NeedsRevie', 'Point_ID', 'FID_Buildi', 'CircleBuil',
  'ShapeSTAre', 'ShapeSTLen' ])

address = address.drop(columns=['AddressNum', 'StreetNa_6', 'Subaddress', 'Subaddre_3', 'Subaddre_4', 'Subaddre_6', 'Subaddre_7', 'Community_', 
    'USPS_Place', 'County_Pla', 'AddressAut', 'LocationDe', 'index'])

# Expand infromation from LOCATION columns that could be used later
colnames = address.columns.tolist()
colnames.extend(['temp_number', 'temp_unit', 'temp_street', 'temp_city'])
address = address.reindex(columns = colnames, fill_value = None)
address.loc[:,['temp_number', 'temp_unit', 'temp_street', 'temp_city']] = [parseLocation(item) for item in address.loc[:,'LOCATION']]

# Fix subadress numbers
address.loc[:,'Subaddre_1'] = [fixSubaddress(item) for item in address.loc[:,'Subaddre_1']]

# Fill in some information that is missing
# If the municipal tag is missing, use from LOCATION and TOWN tags
address.loc[address['Municipal_'].isnull(), 'Municipal_'] = address.loc[address['Municipal_'].isnull(), 'temp_city']
address.loc[address['Municipal_'].isnull(), 'Municipal_'] = address.loc[address['Municipal_'].isnull(), 'TOWN']
# If street is missing use info that is in LOCATION
address.loc[address['CompleteSt'].isnull(), 'CompleteSt'] = address.loc[address['CompleteSt'].isnull(), 'temp_street']
# If housenumber is missing use info that is in LOCATION
address.loc[address['CompleteAd'].isnull(), 'CompleteAd'] = address.loc[address['CompleteAd'].isnull(), 'temp_number']
# If unit is missing use info that is in Subaddre_1
address.loc[address['temp_unit'].isnull(), 'temp_unit'] = address.loc[address['temp_unit'].isnull(), 'Subaddre_1']

# Convert address values
address.loc[:,'addr:street'] = [expandSuffix(item) for item in address.loc[:,'CompleteSt']]
address.loc[:,'addr:housenumber'] = address.loc[:,'CompleteAd']
address.loc[:,'addr:postcode'] = address.loc[:,'ZipCode']
address.loc[:,'addr:city'] = address.loc[:,'Municipal_']
address.loc[:,'addr:unit'] = address.loc[:,'temp_unit']

# Additional fixes:
address.loc[address['addr:street'] == "Old Post Road #", 'addr:street'] = "Old Post Road No 3"
address.loc[address['addr:street'] == "Old Post Rd(6)", 'addr:street'] = "Old Post Road 6"
address.loc[address['addr:street'] == "Wishing Well Lane #7", 'addr:street'] = "Wishing Well Lane"
address.loc[address['addr:street'] == "009A Tory Lane", 'addr:housenumber'] = "9A"
address.loc[address['addr:street'] == "009A Tory Lane", 'addr:street'] = "Tory Lane"
address.loc[address['addr:street'] == "Kent Road (Park)", 'addr:street'] = "Kent Road"
address.loc[address['addr:street'] == "Old Post Rd(2)", 'addr:street'] = "Old Post Road No 2"
address.loc[address['addr:street'] == "Old Post Rd(3)", 'addr:street'] = "Old Post Road No 3"
address.loc[address['addr:street'] == "Deer Run Rd(Rear)", 'addr:street'] = "Deer Run Road"
address.loc[address['addr:street'] == "Father Peter'S", 'addr:street'] = "Father Peter's"
address.loc[address['addr:city'] == "Wesrport", 'addr:city'] = "Westport"
address.loc[address['addr:street'] == "Bunmpy Lane", 'addr:street'] = "Bumpy Lane"
address.loc[address['addr:street'] == "Tod'S Driftway", 'addr:street'] = "Tod's Driftway"
address.loc[address['addr:street'] == "Quarry Road(Turkey Plain", 'addr:street'] = "Quarry Road"
address['addr:street'] = address['addr:street'].str.replace("'S", "'s")
address.loc[address['addr:unit'].isin(['Rd(1-3-5-7)', 'Rd(9-11-19)','Ridge-Wilton', 'Dr-Wilton', 'Rd-New', '-', 
    'Rd-Darien', 'Rd-S', 'Rd-N', 'La-E', 'La-W', '103-E','Rd34-6', '-Wspt']), 'addr:unit'] = None


# Remove extra columns
address = address.drop(columns=['TOWN', 'TOWN_NO', 'LOCATION', 'temp_number', 'temp_street', 'temp_city', 'temp_unit', 'Municipal_', 'E911_Place', 'ZipCode',
    'ZipPlus4', 'AddressFea', 'Comments', 'CompleteAd', 'CompleteSt', 'LandmarkNa', 'AddressN_1','StreetName', 'AddressN_2', 'StreetNa_1',
    'StreetNa_2', 'StreetNa_3', 'StreetNa_4', 'StreetNa_5', 'Subaddre_1', 'Source_Joi', 'Source_J_1', 'Source_J_2'])

# Convert to WGS84
address.crs = "EPSG:4326"



# Save intermediate step
#address.to_file('Address-parsed.shp')
address.to_file('Address-parsed.geojson', driver='GeoJSON')


# Calculate area of buildings
address['area'] = address.geometry.area



# Adresses are duplicated: All buildings on one parcel are tagged with the same address
# For buildings witch address countains housenumber remove duplicates by keeping only that building that has the largest area (most probably the main house on the parcel)
# First convert None to "none" otherwise groupby throws an error (groupby converts None to 'nan', which it can't later find in the grouping index)
address_dedup = address.fillna("none")
# Deduplicate addresses with houssenumber
address_dedup = address_dedup.loc[ address['addr:housenumber'].notnull() ].groupby(['addr:street', 'addr:housenumber', 'addr:postcode', 'addr:city', 'addr:unit'], dropna = False).apply(func = lambda x: x.loc[ x['area'] == x['area'].max() ])
address_remain = address.loc[address['addr:housenumber'].isnull()]
# Convert "none" back to None
#address_dedup.replace(to_replace = "none", value = None, inplace = True)
address_dedup = address_dedup.stack()
address_dedup[address_dedup == "none"] = None
address_dedup = address_dedup.unstack()


# Combine deduplicated addresses with those that don't have house number
address_dedup = pd.concat([address_remain, address_dedup]).pipe(gpd.GeoDataFrame)
address_dedup = address_dedup.reset_index()

# Calculate centroid of the building and set it as address associated geometry
address_dedup['geometry'] = address_dedup.geometry.centroid

# Drop parcell address position information (might still be usefull for some addresses)
address_dedup = address_dedup.drop(columns=['AddressLon', 'AddressLat', 'area', 'index'])

# Drop address points that have only city tag, but no street and housenumber
address_dedup = address_dedup.loc[address_dedup['addr:street'].notnull() | address_dedup['addr:housenumber'].notnull()]

address_dedup.crs = "EPSG:4326"
address_dedup.to_file('Address-dedup-noCity.geojson', driver='GeoJSON')



# Concatenate address dataset with buildings dataset
building = gpd.read_file("Buildings-parsed.geojson")

combined = pd.concat([building, address_dedup]).pipe(gpd.GeoDataFrame)

combined.to_file('Buildings-Address-combined.geojson', driver='GeoJSON')
