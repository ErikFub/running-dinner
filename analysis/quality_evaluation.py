import numpy as np
from data_access.optimal_solution import OptimalSolutionAccess


class QualityEvaluator:
    def __init__(self):
        self.allocation_matrices = OptimalSolutionAccess().get_allocation_matrices()

    def run_check(self):
        sum_matrix = self.sum_of_matrices()
        for col in range(sum_matrix.shape[1]):
            col_sum = int(np.sum(sum_matrix[:, col]))
            if col_sum not in [0, 3]:
                print(f"Error for column with index {col}, only {col_sum} values")
        if np.sum(sum_matrix) != 3**3:
            print(f"Only {int(np.sum(sum_matrix))} instead of {3**3} values in matrix")

    def sum_of_matrices(self):
        sum_matrix = np.zeros(self.allocation_matrices[1].shape)
        for stage in self.allocation_matrices:
            sum_matrix += self.allocation_matrices[stage]
        #print(sum_matrix)
        return sum_matrix

    def print_matrices(self):
        for stage in self.allocation_matrices:
            print(self.allocation_matrices[stage])

