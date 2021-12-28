import numpy as np
from data_access.optimal_solution import OptimalSolutionAccess


class QualityEvaluator:
    def __init__(self):
        self.allocation_matrices = OptimalSolutionAccess().get_allocation_matrices()
        print(self.allocation_matrices)

    def sum_of_matrices(self):
        sum_matrix = np.zeros(self.allocation_matrices[1].shape)
        for stage in self.allocation_matrices:
            sum_matrix += self.allocation_matrices[stage]
        return sum_matrix

print((QualityEvaluator().sum_of_matrices()))