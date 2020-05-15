# WestCOG_buildings
Converting tagging to OSM style


Ways marked as `FCODE=building footprint, Structure under construction, Foundation, Structure ruin, Overhead walkway, Other structure`, which will be tagged as `building=yes`. Ways that touch (share a line segment) will be tagged with `building:part=yes` and a single way made from their union will created and tagged as `building=yes`.

Ways marked as `FCODE=Patio, Deck, House trailer, Tank` will be omitted.

Tags conversion:

Height `BLDGHEIGHT=*` in feet, which will be converted to meters and tagged as `height=*`
Elevation at ground level `BLDG_GNDEL=*`, which will be converted to `ele=*`
Elevation at top of building part `BLDG_TOPEL=*`. This will be removed.
Other tags `OBJECTID=*, Shape_Area=*, Shape_Leng=*` will be removed.
