from shapely.ops import LineString
from shapely import wkb

def function(tc_track, geom_with_crs):
    points = []
    # NB: assumption here is all geometry data is in the same CRS
    _, srid = geom_with_crs

    tc_track.sort(key=lambda x: x['line'])

    for location in tc_track:
        # note the RS geometry type gets passed through as a Python tuple of WKB
        bytes, _ = location['geom']
        points.append(wkb.loads(bytes))
        
    return LineString(points).wkb, srid

