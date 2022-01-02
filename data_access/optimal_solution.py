import json
import os
import numpy as np
from data_access.precomputation import PrecomputationDataAccess
from data_models import OptimalSolution


class OptimalSolutionAccess:
    def __init__(self):
        self.project_directory = os.getenv('project_directory')

    def load_optimal_solution(self) -> OptimalSolution:
        metadata = self.get_metadata()
        return OptimalSolution(allocation_matrices=self.get_allocation_matrices(),
                               nodes=self.get_nodes(),
                               prefiltered=metadata['prefiltered'],
                               costs=metadata['costs'],
                               n_iter=metadata['n_iter'],
                               n_teams=metadata['n_teams'],
                               n_participants=metadata['n_participants'],
                               n_locations=metadata['n_locations'])

    def get_allocation_matrices(self) -> np.array:
        files = os.listdir(f"{self.project_directory}/sample_data/optimal_solution")
        allocation_files = [f for f in files if f[:5] == 'stage']
        allocation_matrices = {}
        for file in allocation_files:
            stage = int(file[-5])
            with open(f'{self.project_directory}/sample_data/optimal_solution/{file}', 'rb') as f:
                matrix = np.load(f)
            allocation_matrices[stage] = matrix
        return allocation_matrices

    def get_nodes(self) -> np.array:
        with open(f'{self.project_directory}/sample_data/optimal_solution/nodes.npy', 'rb') as f:
            nodes = np.load(f)
        return nodes

    def get_polylines_matrix(self, nodes: np.array = None) -> np.array:
        with open(f'{self.project_directory}/sample_data/polylines_matrix.npy', 'rb') as f:
            polylines_matrix = np.load(f)
        if not np.any(nodes):
            return polylines_matrix
        else:
            return polylines_matrix[nodes, :][:, nodes]

    def get_polylines_final_dest(self, nodes: np.array = None) -> np.array:
        with open(f'{self.project_directory}/sample_data/polylines_final_dest.npy', 'rb') as f:
            polylines_final_dest = np.load(f)
        if not np.any(nodes):
            return polylines_final_dest
        else:
            return polylines_final_dest[nodes]

    def get_metadata(self) -> dict:
        with open(f'{self.project_directory}/sample_data/optimal_solution/metadata.json', 'r') as f:
            metadata = json.load(f)
        return metadata

    def save(self, optimizer) -> None:
        for stage in optimizer.best_allocation:
            with open(f'{self.project_directory}/sample_data/optimal_solution/stage_{stage}.npy', 'wb') as f:
                np.save(f, optimizer.best_allocation[stage])
        with open(f'{self.project_directory}/sample_data/optimal_solution/nodes.npy', 'wb') as f:
            if optimizer.prefilter:
                nodes = [PrecomputationDataAccess().get_filtered_nodes()[n] for n in optimizer.best_allocation_teams]
            else:
                nodes = optimizer.best_allocation_teams
            np.save(f, np.array(nodes))
        with open(f'{self.project_directory}/sample_data/optimal_solution/metadata.json', 'w') as f:
            json.dump(self._construct_metadata(optimizer), f)

    @staticmethod
    def _construct_metadata(optimizer) -> dict:
        metadata = {
            "n_teams": optimizer.n_teams,
            "n_participants": optimizer.n_participants,
            "n_locations": optimizer.n_locations,
            "n_iter": optimizer.n_iter,
            "prefiltered": optimizer.prefilter,
            "costs": optimizer.lowest_costs
        }
        return metadata
