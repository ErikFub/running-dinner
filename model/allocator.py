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
        self.n_participants = self.matrix.distances.shape[0]
        self.n_locations = math.floor(self.n_participants / n_rounds / n_team_members)
        self.n_teams = self.n_locations * n_rounds
        self.allocation_matrices = {}
        self.visited_locations = []
        self.stage_hosts = {}
        self.eligible_teams = []
        self.met_teams = {i: set() for i in range(self.n_teams)}
        self.actual_distances = {}
        self.eligible_teams_distances = None
        self.lowest_costs = math.inf
        self.best_allocation = None

    def print_stats(self):
        print("Participants:", self.n_participants)
        print("Locations per Round:", self.n_locations)
        print("Teams:", self.n_teams)

    def run_and_evaluate_sample(self):
        self.allocate_last_stage()
        self.allocate_mid_stages()
        self.allocate_first_stage()
        self.get_actual_distances()
        costs = self.evaluate_allocation()
        if costs < self.lowest_costs:
            self.best_allocation = self.allocation_matrices.copy()
            self.lowest_costs = costs
        self.reset()


    def allocate_last_stage(self):
        nearest_locations = np.argpartition(self.matrix.distances_final_dest, self.n_locations)[:self.n_locations]
        self.stage_hosts[self.n_rounds] = nearest_locations
        self.eligible_teams += nearest_locations.tolist()
        self.visited_locations += nearest_locations.tolist()
        allocation_matrix = self.create_host_matrix(range(len(nearest_locations)))
        self.eligible_teams += np.random.choice([i for i in range(self.n_participants) if i not in nearest_locations],
                                                self.n_teams - self.n_locations, replace=False).tolist()
        allocation_matrix = self.allocate_guests(allocation_matrix, self.n_rounds)
        self.allocation_matrices[self.n_rounds] = allocation_matrix
        #print(allocation_matrix)
        #print(self.visited_locations)

    def allocate_mid_stages(self):
        mid_stages = range(self.n_rounds+1)[2:-1]
        for stage in mid_stages:
            eligible_hosts = [i for i, t in enumerate(self.eligible_teams) if t not in self.visited_locations]
            chosen_hosts = np.random.choice(eligible_hosts, self.n_rounds, replace=False)
            chosen_hosts_num = [self.eligible_teams[i] for i in chosen_hosts]
            self.stage_hosts[stage] = chosen_hosts_num
            self.visited_locations += chosen_hosts_num
            allocation_matrix = self.create_host_matrix(chosen_hosts)
            self.allocation_matrices[stage] = self.allocate_guests(allocation_matrix, stage)

    def allocate_first_stage(self):
        eligible_hosts = [i for i, t in enumerate(self.eligible_teams) if t not in self.visited_locations]
        chosen_hosts = np.random.choice(eligible_hosts, self.n_rounds, replace=False)
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
        # add constraint: teams that will meet in later stage can't re-meet
        self.update_met_teams()
        success = False
        while not success:
            matrix = host_matrix.copy()
            possible_guests = [i for i, team in enumerate(self.eligible_teams) if team not in self.stage_hosts[stage]]
            for i, row in enumerate(matrix):
                if matrix[i][i] == 1:
                    prohibited_guests = self.met_teams[i].copy()
                    for j in range(self.n_rounds-1):
                        eligible_guests = [g for g in possible_guests if g not in prohibited_guests]
                        if len(eligible_guests) == 0:
                            break
                        else:
                            guest = np.random.choice(eligible_guests, replace=False)
                            possible_guests.remove(guest)
                            prohibited_guests.update(self.met_teams[guest])
                            matrix[guest][i] = 1
            else:
                success = True
        return matrix

    def update_met_teams(self):
        for stage in self.allocation_matrices.keys():
            allocation_matrix = self.allocation_matrices[stage]
            for i in range(allocation_matrix.shape[0]):
                col = allocation_matrix[:, i]
                for j, val in enumerate(col):
                    if val == 1:
                        covisited = [k for k, v in enumerate(col) if v == 1 and k != j]
                        # met teams = index in allocation matrix, not team num
                        self.met_teams[j].update(covisited)

    def _get_eligible_teams_distances(self):
        self.eligible_teams_distances = self.matrix.distances[self.eligible_teams, :][:, self.eligible_teams]

    def get_actual_distances(self):
        self._get_eligible_teams_distances()
        for i in range(self.n_rounds):
            stage = i+1
            if stage == 1:
                self.actual_distances[stage] = np.zeros(self.eligible_teams_distances.shape)
            else:
                allocation_matrix = self.allocation_matrices[stage-1].copy()
                actual_distances = np.zeros(self.eligible_teams_distances.shape)
                for team_idx, row in enumerate(allocation_matrix):
                    host_idx = np.argmax(row)
                    actual_distances[team_idx] = self.eligible_teams_distances[host_idx]
                self.actual_distances[stage] = actual_distances

    def evaluate_allocation(self):
        total_costs = 0
        for stage in self.allocation_matrices.keys():
            costs = np.sum(self.allocation_matrices[stage] * self.eligible_teams_distances[stage])
            total_costs += costs
        return total_costs

    def reset(self):
        self.allocation_matrices = {}
        self.visited_locations = []
        self.stage_hosts = {}
        self.eligible_teams = []
        self.met_teams = {i: set() for i in range(self.n_teams)}
        self.actual_distances = {}
        self.eligible_teams_distances = None

    def save_best_allocations(self):
        for stage in self.best_allocation.keys():
            with open(f'sample_data/best_allocations/stage_{stage}.npy', 'wb') as f:
                np.save(f, self.best_allocation[stage])


