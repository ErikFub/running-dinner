from data_access.survey_response import SurveyResponseAccess
from data_access.final_dest import FinalDestination
from model.distance_matrix import DistanceMatrix
from model.allocator import Allocator
from tqdm import tqdm
from analysis.visualization.visualization import MapVisualization


def retrieve_data_from_api():
    data = SurveyResponseAccess.get_data_dummy()
    final_dest = FinalDestination()
    matrix = DistanceMatrix(data, final_dest)
    matrix.save()


def run_from_sample():
    matrix = DistanceMatrix()
    allocator = Allocator(matrix)
    for i in tqdm(range(1000)):
        allocator.run_and_evaluate_sample()
    allocator.save_best_allocations()
    lowest_costs = allocator.lowest_costs
    print(f"Lowest costs: {lowest_costs}, i.e. on average {round(lowest_costs/allocator.n_teams/60,2)} min per person")


def visualize():
    MapVisualization().create()


if __name__ == "__main__":
    #retrieve_data_from_api()
    run_from_sample()
    visualize()
