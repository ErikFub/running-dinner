import polyline
import json
import os
import numpy as np
import random
from data_access.optimal_solution import OptimalSolutionAccess


class GeoJsonCreator:
    def __init__(self):
        self.save_location = f"{os.getenv('project_directory')}/analysis/visualization/JS/geo_json.js"
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
                                "marker-color": color,
                                "marker-size": "medium",
                                "marker-symbol": "",
                                "stroke": "#555555",
                                "stroke-width": 2,
                                "stroke-opacity": 1
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": list(coords[point_idx])
                            }}
        self.geo_json['features'].append(geo_json_feature)

    def save(self):
        with open(self.save_location, 'w') as file_handler:
            file_handler.write(f'var all_turfs = {str(json.dumps(self.geo_json))}')


class MapVisualization:
    def __init__(self):
        self.polylines_matrix, self.final_dest_polylines, self.best_allocations, self.nodes = self._get_data()
        self.actual_polylines = {}
        self.get_actual_polylines()

    def get_actual_polylines(self):
        for stage in self.best_allocations:
            if stage == 1:
                self.actual_polylines[stage] = np.empty(self.polylines_matrix.shape, dtype='<U5000')
            else:
                allocation_matrix = self.best_allocations[stage-1].copy()
                actual_polylines = np.empty(self.polylines_matrix.shape, dtype='<U5000')
                for team_idx, row in enumerate(allocation_matrix):
                    host_idx = np.argmax(row)
                    actual_polylines[team_idx] = self.polylines_matrix[host_idx]
                self.actual_polylines[stage] = actual_polylines

    def _get_random_color(self):
        r = lambda: random.randint(0, 255)
        return '#%02X%02X%02X' % (r(), r(), r())

    def create(self):
        geo_json = GeoJsonCreator()
        for stage in self.best_allocations:
            if stage == 1:
                allocation_matrix = self.best_allocations[2]
                stage_color = self._get_random_color()
                for r in range(allocation_matrix.shape[0]):
                    for c in range(allocation_matrix.shape[1]):
                        if allocation_matrix[r][c] == 1 and r != c:
                            pline = self.actual_polylines[2][r][c]
                            geo_json.create_point_from_polyline(pline, color=stage_color, point_idx=0)
            if stage > 1:
                allocation_matrix = self.best_allocations[stage]
                stage_color = self._get_random_color()
                for r in range(allocation_matrix.shape[0]):
                    for c in range(allocation_matrix.shape[1]):
                        if allocation_matrix[r][c] == 1 and r != c:
                            pline = self.actual_polylines[stage][r][c]
                            geo_json.create_polyline(pline, color=stage_color)
                            geo_json.create_point_from_polyline(pline, color=stage_color)
        last_stage = max(self.best_allocations.keys())
        last_matrix = self.best_allocations[last_stage]
        for r in range(last_matrix.shape[0]):
            for c in range(last_matrix.shape[1]):
                if last_matrix[r][c] == 1 and r != c:
                    pline = self.final_dest_polylines[c]
                    geo_json.create_polyline(pline)
                    geo_json.create_point_from_polyline(pline)
        geo_json.save()

    @staticmethod
    def _get_data():
        optimal_solution = OptimalSolutionAccess()
        allocation_matrices = optimal_solution.get_allocation_matrices()
        nodes = optimal_solution.get_nodes()
        polylines_matrix = optimal_solution.get_polylines_matrix(nodes)
        polylines_final_dest = optimal_solution.get_polylines_final_dest(nodes)
        return polylines_matrix, polylines_final_dest, allocation_matrices, nodes