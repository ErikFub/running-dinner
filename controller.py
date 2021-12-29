from data_access.survey_response import SurveyResponseAccess
from data_access.final_dest import FinalDestination
from model.distance_matrix import DistanceMatrix
from model.optimizer import Optimizer
from analysis.visualization.visualization import MapVisualization
from analysis.quality_evaluation import QualityEvaluator


def retrieve_data_from_api():
    nodes = SurveyResponseAccess.get_data_dummy()
    final_dest = FinalDestination()
    matrix = DistanceMatrix(nodes, final_dest)
    matrix.save()


def run_from_sample():
    n_trials = 1_000_000
    matrix = DistanceMatrix()
    optimizer = Optimizer(matrix, n_iter=n_trials)
    #optimizer.print_stats()
    optimizer.run(progress_bar=True, prefilter=True, load_precomputed=True)
    #optimizer.run_parallel(progress_bar=False, prefilter=True, load_precomputed=True)
    optimizer.save_best_allocations()
    lowest_costs = optimizer.lowest_costs
    print(f"Lowest costs: {lowest_costs}, i.e. on average {round(lowest_costs/optimizer.n_teams/60,2)} min per person")


def evaluate():
    qe = QualityEvaluator()
    qe.print_matrices()
    qe.run_check()


def visualize():
    MapVisualization().create()


if __name__ == "__main__":
    # retrieve_data_from_api()
    run_from_sample()
    # evaluate()
    visualize()
