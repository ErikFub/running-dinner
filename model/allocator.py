import numpy as np
import random
from model.distance_matrix import DistanceMatrix


class Allocator:
    def __init__(self, matrix: DistanceMatrix, n_rounds: int, n_locations: int):
        self.matrix = matrix
        self.n_rounds = n_rounds
        self.n_locations = n_locations
        self.n_teams = self.n_locations * n_rounds
        self.allocation_matrices = {}
        self.visited_locations = []
        self.stage_hosts = {}
        self.eligible_teams = []
        self.met_teams = {i: set() for i in range(self.n_teams)}

    def get_feasible_solution(self):
        self.allocate_last_stage()
        self.allocate_mid_stages()
        self.allocate_first_stage()
        return self.allocation_matrices, self.eligible_teams

    def allocate_last_stage(self):
        teams_partitioned = np.argpartition(self.matrix.distances_final_dest, self.n_locations)
        nearest_locations = teams_partitioned[:self.n_locations]
        remaining_locations = teams_partitioned[self.n_locations:]
        self.stage_hosts[self.n_rounds] = nearest_locations
        self.eligible_teams += nearest_locations.tolist()
        self.visited_locations += nearest_locations.tolist()
        allocation_matrix = self.create_host_matrix(range(self.n_locations))
        self.eligible_teams += random.sample(remaining_locations.tolist(), k=(self.n_teams - self.n_locations))
        allocation_matrix = self.allocate_guests(allocation_matrix, self.n_rounds)
        self.allocation_matrices[self.n_rounds] = allocation_matrix

    def allocate_mid_stages(self):
        mid_stages = range(self.n_rounds+1)[2:-1]
        for stage in mid_stages:
            eligible_hosts = [i for i, t in enumerate(self.eligible_teams) if t not in self.visited_locations]
            chosen_hosts = np.random.choice(eligible_hosts, self.n_locations, replace=False)
            chosen_hosts_num = [self.eligible_teams[i] for i in chosen_hosts]
            self.stage_hosts[stage] = chosen_hosts_num
            self.visited_locations += chosen_hosts_num
            allocation_matrix = self.create_host_matrix(chosen_hosts)
            self.allocation_matrices[stage] = self.allocate_guests(allocation_matrix, stage)

    def allocate_first_stage(self):
        eligible_hosts = [i for i, t in enumerate(self.eligible_teams) if t not in self.visited_locations]
        chosen_hosts = np.random.choice(eligible_hosts, self.n_locations, replace=False)
        chosen_hosts_num = [self.eligible_teams[i] for i in chosen_hosts]
        self.stage_hosts[1] = chosen_hosts_num
        self.visited_locations += chosen_hosts_num
        allocation_matrix = self.create_host_matrix(chosen_hosts)
        self.allocation_matrices[1] = self.allocate_guests(allocation_matrix, 1)

    def create_host_matrix(self, hosts):
        matrix = np.zeros((self.n_teams, self.n_teams))
        for host in hosts:
            matrix[host][host] = 1
        return matrix

    def allocate_guests(self, host_matrix, stage):
        self.update_met_teams_b()
        matrix = host_matrix.copy()
        possible_guests = [i for i, team in enumerate(self.eligible_teams) if team not in self.stage_hosts[stage]] # get all teams that are not hosts in that round
        for i, row in enumerate(matrix):
            if matrix[i][i] == 1:
                prohibited_guests = self.met_teams[i].copy()
                for j in range(self.n_rounds-1):
                    eligible_guests = [g for g in possible_guests if g not in prohibited_guests]
                    if len(eligible_guests) == 0:
                        # if based on prior allocation no allocation in which teams don't see each other 2 times is
                        # possible, then return a 2s matrix. Allocation will be discarded as costs are too high.
                        return np.full(matrix.shape, 2)
                    else:
                        guest = np.random.choice(eligible_guests)
                        possible_guests.remove(guest)
                        prohibited_guests.update(self.met_teams[guest])
                        matrix[guest][i] = 1
        return matrix

    def update_met_teams(self):
        for stage in self.allocation_matrices:
            allocation_matrix = self.allocation_matrices[stage]
            for i in range(allocation_matrix.shape[0]):
                col = allocation_matrix[:, i]
                for j, val in enumerate(col):
                    if val == 1:
                        covisited = [k for k, v in enumerate(col) if v == 1 and k != j]
                        # met teams = index in allocation matrix, not team num
                        self.met_teams[j].update(covisited)

    def update_met_teams_b(self):
        for stage in self.allocation_matrices:
            allocation_matrix = self.allocation_matrices[stage]
            allocations = np.transpose(np.nonzero(allocation_matrix == 1))
            for allocation in allocations:
                covisitors = allocations[(allocations[:, 1] == allocation[1]) & (allocations[:, 0] != allocation[0])][:,0]
                self.met_teams[allocation[0]].update(covisitors)
