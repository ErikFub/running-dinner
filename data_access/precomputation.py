import os
import numpy as np


class PrecomputationDataAccess:
    def __init__(self):
        self.project_directory = os.getenv('project_directory')

    def get_filtered_nodes(self) -> list:
        with open(f'{self.project_directory}/sample_data/precomputation/filtered_nodes.npy', 'rb') as f:
            filtered_nodes = np.load(f)
        return list(filtered_nodes)

    def save_filtered_nodes(self, filtered_nodes: list) -> None:
        filtered_nodes = np.array(filtered_nodes)
        with open(f'{self.project_directory}/sample_data/precomputation/filtered_nodes.npy', 'wb') as f:
            np.save(f, filtered_nodes)
