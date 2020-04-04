# WestCOG_buildings
Converting tagging to OSM style


Dataset consists of building parts marked as FCODE=building footprint, which will be converted to building:part=yes. Each contain information about building part:

Height `BLDGHEIGHT=*` in feet, which will be converted to meters and tagged as `height=*`
Elevation at ground level `BLDG_GNDEL=*`, which will be converted to `ele=*`
Elevation at top of building part `BLDG_TOPEL=*`. This will be removed.
Other tags `OBJECTID=*, Shape_Area=*, Shape_Leng=*` will be removed.

A copy of all building parts of of each building will be merged into a single union building footprint, tagged as `building=yes` and nodes will be merged with nodes belonging to `building:part=yes` objects.

Building parts marked as `FCODE=Patio, Deck, House trailer, Tank` will be omitted. Other building parts marked as e.g. `FCODE=Structure ruin, Overhead walkway, Other structure`, will be omitted or included by importing user based on available imagery.


Import will follow using JOSM:
1. Load .shp file
2. Select all objects labeled with 'building_p' and rename to 'building:part'
3. Run Validator
4. Fix any ovelapping builidings, overlapping nodes, etc.
5. Upload
