import math

import numpy as np
import random
from model.distance_matrix import DistanceMatrix
from tqdm import tqdm


class Allocator:
    def __init__(self, matrix: DistanceMatrix, n_rounds: int = 3, n_team_members: int = 2):
        self.matrix = matrix
        self.n_rounds = n_rounds
        self.n_team_members = n_team_members
        self.allocation_matrices = {}
        self.visited_locations = []

    def get_random_allocation(self):
        possible_rows = []
        for i in range(self.matrix.distances.shape[0]):
            row = list(np.zeros(self.matrix.distances.shape[0]))
            row[i] = 1
            possible_rows.append(row)

        meets_requirements = False
        while not meets_requirements:
            allocation_matrix = np.array(random.choices(possible_rows, k=self.matrix.distances.shape[1]))
            meets_requirements = np.all(np.logical_or(np.sum(allocation_matrix, axis=0) == 0,
                                                      np.sum(allocation_matrix, axis=0) == 3))

        return allocation_matrix

    def construct_feasible_allocation(self):
        n_locations = math.floor(self.matrix.distances.shape[0]/self.n_rounds/self.n_team_members) # needs division by two to account for n_team_mebers
        available_hosts = [h for h in range(self.matrix.distances.shape[0]) if h not in self.visited_locations]
        hosts = np.random.choice(available_hosts, n_locations, replace=False)
        allocation_matrix = np.zeros(self.matrix.distances.shape)
        for host in hosts:
            allocation_matrix[host][host] = 1
        for host in hosts:
            unassigned = [i for i in range(len(np.sum(allocation_matrix, axis=1))) if np.sum(allocation_matrix, axis=1)[i] == 0]
            guests = np.random.choice(unassigned, (self.n_rounds*self.n_team_members)-1, replace=False)
            for guest in guests:
                allocation_matrix[guest][host] = 1
        return allocation_matrix


    def get_best_allocations(self, stage: int):
        lowest_cost = math.inf
        best_allocation = None
        for i in tqdm(range(20000)):
            allocation_matrix = self.construct_feasible_allocation()
            cost = np.sum(allocation_matrix*self.matrix.distances)
            if cost < lowest_cost:
                lowest_cost = cost
                best_allocation = allocation_matrix
        self.allocation_matrices[stage] = best_allocation
        self.update_distance_matrix(stage)
        self.visited_locations += [i for i in range(best_allocation.shape[0]) for j in range(best_allocation.shape[1]) if i == j and best_allocation[i][j] == 1]
        print(lowest_cost)
        #print(best_allocation)
        #print(self.matrix.distances)
        #print(self.visited_locations)

    def update_distance_matrix(self, stage: int):
        distances = self.matrix.distances.copy()
        allocation = self.allocation_matrices[stage]
        for i, row in enumerate(allocation):
            current_location = np.argmax(row)
            self.matrix.distances[i] = distances[current_location]

    @staticmethod
    def load_dummies():
        with open('sample_data/allocation_matrices.npy', 'rb') as f:
            allocation_matrices = np.load(f)
        return allocation_matrices

