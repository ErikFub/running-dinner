from data_access.survey_response import SurveyResponseAccess
from data_access.final_dest import FinalDestination
from model.distance_matrix import DistanceMatrix
from model.allocator import Allocator
import numpy as np
from tqdm import tqdm
from data_access.google_maps_api import GoogleMapsAPI

#data = SurveyResponseAccess.get_data_dummy()
#final_dest = FinalDestination()
#matrix = DistanceMatrix(data, final_dest)
#matrix.save()

matrix = DistanceMatrix()

allocator = Allocator(matrix)
for i in tqdm(range(10000)):
    allocator.run_and_evaluate_sample()
lowest_costs = allocator.lowest_costs
print(f"Lowest costs: {lowest_costs}, i.e. on average {round(lowest_costs/allocator.n_teams/60,2)} min per person")
