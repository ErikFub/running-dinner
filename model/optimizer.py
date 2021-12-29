from model.allocator import Allocator
from model.evaluator import Evaluator
import math
from tqdm import tqdm
from model.distance_matrix import DistanceMatrix
from data_access.optimal_solution import OptimalSolutionAccess
from data_access.precomputation import PrecomputationDataAccess
from joblib import Parallel, delayed


class Optimizer:
    def __init__(self, matrix: DistanceMatrix, n_rounds: int = 3, n_team_members: int = 2, n_iter: int = 10000):
        self.matrix = matrix
        self.n_iter = n_iter
        self.n_rounds = n_rounds
        self.n_participants = self.matrix.distances.shape[0]
        self.n_locations = math.floor(self.n_participants / n_rounds / n_team_members)
        self.n_teams = self.n_locations * n_rounds
        self.lowest_costs = math.inf
        self.best_allocation = None
        self.best_allocation_teams = None

    def print_stats(self):
        print("Participants:", self.n_participants)
        print("Locations per Round:", self.n_locations)
        print("Teams:", self.n_teams)

    def run(self, progress_bar: bool = False, prefilter: bool = False):
        if prefilter:
            self.prefilter_nodes(load_precomputed=False)
        iterator = tqdm(range(self.n_iter)) if progress_bar else range(self.n_iter)
        for i in iterator:
            allocator = Allocator(self.matrix, self.n_rounds, self.n_locations)
            allocations, nodes = allocator.get_feasible_solution()
            costs = Evaluator(self.matrix.distances, allocations, nodes).get_costs()
            if costs < self.lowest_costs:
                self.best_allocation = allocations
                self.best_allocation_teams = nodes
                self.lowest_costs = costs

    def prefilter_nodes(self, load_precomputed: bool = True, progress_bar: bool = True):
        if load_precomputed:
            filtered_teams = PrecomputationDataAccess().get_filtered_nodes()
        else:
            def run_rep(matrix, n_rounds, n_locations, n_iter):
                base_optimization_iter_mult = 1
                base_iter = int(base_optimization_iter_mult * n_iter)
                rep_costs = math.inf
                rep_best_teams = None
                for i in range(base_iter):
                    allocator = Allocator(matrix, n_rounds, n_locations)
                    allocations, nodes = allocator.get_feasible_solution()
                    costs = Evaluator(matrix.distances, allocations, nodes).get_costs()
                    if costs < rep_costs:
                        rep_costs = costs
                        rep_best_teams = nodes
                return rep_best_teams

            reps = 10
            best_team_constellations = Parallel(n_jobs=5, verbose=20)\
                (delayed(run_rep)(self.matrix, self.n_rounds, self.n_locations, self.n_iter) for i in range(reps))
            filtered_teams = list(set([t for constellation in best_team_constellations for t in constellation]))
            PrecomputationDataAccess().save_filtered_nodes(filtered_teams)
        print(f"Filtered out nodes: {self.n_participants - len(filtered_teams)}")
        self.matrix.filter(filtered_teams)

    def save_best_allocations(self):
        OptimalSolutionAccess().save(self.best_allocation, self.best_allocation_teams)
