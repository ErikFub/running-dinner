import numpy as np
from data_access.google_maps_api import GoogleMapsAPI
from data_access.survey_response import Participant
from data_access.final_dest import FinalDestination


class DistanceMatrix:
    def __init__(self, matrix_data: list[Participant] = None, final_dest: FinalDestination = None):
        if not matrix_data or not final_dest:
            self.nodes, self.distances, self.distances_final_dest = self.load_dummies()
        else:
            self.nodes = [((p.first_name + ' ' + p.last_name), p.address) for p in matrix_data]
            self.final_dest_address = final_dest.address
            self.distances, self.distances_final_dest = self.construct()
        #print("Matrix successfully constructed")

    def construct(self):
        num_nodes = len(self.nodes)
        distance_matrix = np.zeros((num_nodes, num_nodes))
        distances_final_dest_matrix = np.zeros(num_nodes)
        maps = GoogleMapsAPI()
        for i, node in enumerate(self.nodes):
            node_address = node[1]
            for j, neighbor in enumerate(self.nodes):
                if i != j:
                    neighbor_address = neighbor[1]
                    distance_matrix[i][j] = maps.get_distance(node_address, neighbor_address)
            distances_final_dest_matrix[i] = maps.get_distance(node_address, self.final_dest_address)
        return distance_matrix, distances_final_dest_matrix

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

    @staticmethod
    def load_dummies():
        with open('sample_data/distances.npy', 'rb') as f:
            matrix = np.load(f)
        with open('sample_data/nodes.npy', 'rb') as f:
            nodes = np.load(f)
        with open('sample_data/distances_final_dest.npy', 'rb') as f:
            matrix_final_dest = np.load(f)
        return nodes, matrix, matrix_final_dest
