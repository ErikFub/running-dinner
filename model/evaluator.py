import numpy as np
from model.distance_matrix import DistanceMatrix


class Evaluator:
    def __init__(self, distances: np.array, allocation_matrices: dict[np.array], teams: list):
        self.allocation_matrices = allocation_matrices
        self.actual_distances = {}
        self.teams_distances = distances[teams, :][:, teams]

    def get_actual_distances(self):
        for stage in self.allocation_matrices:
            if stage == 1:
                self.actual_distances[stage] = self.teams_distances
            else:
                allocation_matrix = self.allocation_matrices[stage - 1].copy()
                actual_distances = np.zeros(self.teams_distances.shape)
                for team_idx, row in enumerate(allocation_matrix):
                    host_idx = np.argmax(row)
                    actual_distances[team_idx] = self.teams_distances[host_idx]
                self.actual_distances[stage] = actual_distances

    def get_costs(self):
        self.get_actual_distances()
        total_costs = 0
        for stage in self.allocation_matrices:
            if stage == 1:
                stage_costs = 0.33 * np.sum(self.allocation_matrices[stage] * self.actual_distances[stage])
            else:
                stage_costs = np.sum(self.allocation_matrices[stage] * self.actual_distances[stage])
            total_costs += stage_costs
        return total_costs
