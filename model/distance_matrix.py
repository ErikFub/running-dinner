import numpy as np
from data_access.google_maps_api import DirectionsAPI
from data_access.survey_response import Participant
from data_access.final_dest import FinalDestination


class DistanceMatrix:
    def __init__(self, matrix_data: list[Participant] = None, final_dest: FinalDestination = None):
        if not matrix_data or not final_dest:
            self.nodes, self.distances, self.distances_final_dest = self.load_dummies()
        else:
            self.nodes = [((p.first_name + ' ' + p.last_name), p.address) for p in matrix_data]
            self.final_dest_address = final_dest.address
            self.distances, self.distances_final_dest, self.polylines_matrix, self.polylines_final_dest_matrix = self.construct()
        #print("Matrix successfully constructed")

    def construct(self):
        num_nodes = len(self.nodes)
        distance_matrix = np.zeros((num_nodes, num_nodes))
        polylines_matrix = np.empty((num_nodes, num_nodes), dtype="<U5000")
        distances_final_dest_matrix = np.zeros(num_nodes)
        polylines_final_dest_matrix = np.empty(num_nodes, dtype="<U5000")
        for i, node in enumerate(self.nodes):
            node_address = node[1]
            for j, neighbor in enumerate(self.nodes):
                if i != j:
                    neighbor_address = neighbor[1]
                    directions_api = DirectionsAPI(node_address, neighbor_address, 'walking')
                    distance_matrix[i][j] = directions_api.distance
                    polylines_matrix[i][j] = directions_api.polyline
            directions_api = DirectionsAPI(node_address, self.final_dest_address, 'walking')
            distances_final_dest_matrix[i] = directions_api.distance
            polylines_final_dest_matrix[i] = directions_api.polyline
        return distance_matrix, distances_final_dest_matrix, polylines_matrix, polylines_final_dest_matrix

    def filter(self, nodes):
        self.distances = self.distances[nodes, :][:, nodes]
        self.distances_final_dest = self.distances_final_dest[nodes]
        self.nodes = self.nodes[nodes]

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
        with open('sample_data/distances_final_dest.npy', 'wb') as f:
            np.save(f, self.distances_final_dest)
        with open('sample_data/polylines_matrix.npy', 'wb') as f:
            np.save(f, self.polylines_matrix)
        with open('sample_data/polylines_final_dest.npy', 'wb') as f:
            np.save(f, self.polylines_final_dest_matrix)


    @staticmethod
    def load_dummies():
        with open('sample_data/distances.npy', 'rb') as f:
            matrix = np.load(f)
        with open('sample_data/nodes.npy', 'rb') as f:
            nodes = np.load(f)
        with open('sample_data/distances_final_dest.npy', 'rb') as f:
            matrix_final_dest = np.load(f)
        return nodes, matrix, matrix_final_dest
