import polyline
import json


class GeoJsonCreator:
    def __init__(self):
        self.geo_json = {
            "type": "FeatureCollection",
            "features": []
        }

    def create_polyline(self, input_polyline: str, color: str = "#555555"):
        coords = polyline.decode(input_polyline, geojson=True)
        geo_json_feature = {"type": "Feature",
                            "properties": {
                                "stroke": color,
                                "stroke-width": 2,
                                "stroke-opacity": 1
                            },
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [list(coord) for coord in coords]
                            }}
        self.geo_json['features'].append(geo_json_feature)

    def create_point_from_polyline(self, input_polyline, color: str = "#555555", point_idx: int = -1):
        coords = polyline.decode(input_polyline, geojson=True)
        geo_json_feature = {"type": "Feature",
                            "properties": {
                                "stroke": color,
                                "stroke-width": 2,
                                "stroke-opacity": 1
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": list(coords[point_idx])
                            }}
        self.geo_json['features'].append(geo_json_feature)

    def save(self):
        with open("C:/Users/erikf/Desktop/running_dinner_assistant/analysis/visualization/JS/geo_json.js", 'w') as file_handler:
            file_handler.write(f'var all_turfs = {str(json.dumps(self.geo_json))}')

line = "ssfkFxj`w@S?KgAMcBMyA_@Jc@NCi@McB_@wBIg@HBG@Km@dA[d@S\\OrFqB_@y@Wq@g@gBLKDENSN_@RcCNuCTiDHu@`@uC`@aC\\{BXwBD[ZcAP_@EW?W@OEyB?qK?wE@eK?uEEoASuCGi@k@qE[yBu@wD_@sAw@_CgCcHqAmDu@qBYkAMu@Oi@Gs@EcACcAZkk@H}PLgC@m@Gs@e@eCODWaBIo@?IFODGLG^KvAg@V]Hi@EuAkAuHk@qDgBkL]yBa@NaCt@eFtAkA\\cCt@_HnBsGlBuAb@CFABL\\}A^]D]iC|A_@J@DD@@PEMaA?KIk@Im@E?I@E?wAa@aAKi@M[IO?G@GDEHGGyAo@[Ka@IkBo@cAe@SFc@PKd@Sn@KT_AdAq@b@O?k@c@g@]K?MBSHCJUXa@Zy@n@WDO\\_AxAY`@GGLAp@aAn@gACgAEi@AEECa@Gq@GGGEGGo@?sA@uA?k@QAA?"
gj = GeoJsonCreator()
gj.create_point_from_polyline(line)
gj.create_polyline(line)
gj.save()