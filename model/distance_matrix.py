import numpy as np
from data_access.google_maps_api import GoogleMapsAPI
from data_access.survey_response import Participant


class DistanceMatrix:
    def __init__(self, matrix_data: list[Participant] = None):
        if not matrix_data:
            self.nodes, self.distances = self.load_dummies()
        else:
            self.nodes = [((p.first_name + ' ' + p.last_name), p.address) for p in matrix_data]
            self.distances = self.construct()

    def construct(self):
        num_nodes = len(self.nodes)
        distance_matrix = np.zeros((num_nodes, num_nodes))
        maps = GoogleMapsAPI()
        for i, node in enumerate(self.nodes):
            for j, neighbor in enumerate(self.nodes):
                if i != j:
                    distance_matrix[i][j] = maps.get_distance(node[1], neighbor[1])
        return distance_matrix

    def print_distances(self):
        for i, node in enumerate(self.nodes):
            print(f"Distances for {node[0]} ({node[1]}):")
            for j, neighbor in enumerate(self.distances[i]):
                if i != j:
                    print(f"\t{int(self.distances[i][j]/60)} min to {self.nodes[j][0]} ({self.nodes[j][1]})")
            print("\n")

    def save(self):
        with open('sample_data/distances.npy', 'wb') as f:
            np.save(f, self.distances)
        with open('sample_data/nodes.npy', 'wb') as f:
            np.save(f, self.nodes)

    @staticmethod
    def load_dummies():
        with open('sample_data/distances.npy', 'rb') as f:
            matrix = np.load(f)
        with open('sample_data/nodes.npy', 'rb') as f:
            nodes = np.load(f)
        return nodes, matrix
