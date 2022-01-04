from dataclasses import dataclass
import numpy as np


@dataclass
class OptimalSolution:
    allocation_matrices: dict[np.array]
    nodes: np.array
    prefiltered: bool
    costs: float
    n_iter: int
    n_teams: int
    n_participants: int
    n_locations: int
