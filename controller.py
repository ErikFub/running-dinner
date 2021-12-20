from data_access.survey_response import SurveyResponseAccess
from model.distance_matrix import DistanceMatrix

data = SurveyResponseAccess.get_data_dummy()
matrix = DistanceMatrix(data)
