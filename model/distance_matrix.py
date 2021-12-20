import numpy as np
from data_access.google_maps_api import GoogleMapsAPI
from data_access.survey_response import Participant


class DistanceMatrix:
    def __init__(self, matrix_data):
        self.matrix = self.construct(matrix_data)

    @staticmethod
    def construct(matrix_data: list[Participant]):
        nodes = [((p.first_name + ' ' + p.last_name), p.address) for p in matrix_data]
        num_nodes = len(nodes)
        distance_matrix = np.zeros((num_nodes, num_nodes))
        maps = GoogleMapsAPI()
        for i, node in enumerate(nodes):
            for j, neighbor in enumerate(nodes):
                if i != j:
                    distance_matrix[i][j] = maps.get_distance(node, neighbor)
        print(distance_matrix)
        return distance_matrix
