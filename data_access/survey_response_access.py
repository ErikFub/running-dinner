import pandas as pd

class SurveyResponseAccess:
    def __init__(self):
        pass

    def get_data(self):
        return pd.read_csv('survey_response_sample.csv')

