# WestCOG_buildings
Converting tagging to OSM style


Ways marked as `FCODE=building footprint, Structure under construction, Foundation, Structure ruin, Overhead walkway, Other structure`, which will be tagged as `building=yes`. Ways that touch (share a line segment) will be tagged with `building:part=yes` and a single way made from their union will created and tagged as `building=yes`.

Ways marked as `FCODE=Patio, Deck, House trailer, Tank` will be omitted.

Tags conversion:

Height `BLDGHEIGHT=*` in feet, which will be converted to meters and tagged as `height=*`
Elevation at ground level `BLDG_GNDEL=*`, which will be converted to `ele=*`
Elevation at top of building part `BLDG_TOPEL=*`. This will be removed.
Other tags `OBJECTID=*, Shape_Area=*, Shape_Leng=*` will be removed.


Import will follow using JOSM:
1. Load .shp file
2. Select all objects labeled with 'building_p' and rename to 'building:part'
3. Run Validator
4. Fix any ovelapping builidings, overlapping nodes, etc.
5. Upload
