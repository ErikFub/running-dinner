import pandas as pd
from dataclasses import dataclass


class SurveyResponseAccess:
    def __init__(self):
        pass

    def get_data(self, deserialized=True):
        pass

    @staticmethod
    def get_data_dummy(deserialized=True):
        data = pd.read_csv('sample_data/survey_response_sample.csv', encoding='latin-1')
        if deserialized:
            # TO CHANGE
            return [Participant.deserialize(response) for response in data.to_numpy().tolist()]
        else:
            return data


@dataclass
class Participant:
    first_name: str
    last_name: str
    address: str

    @staticmethod
    def deserialize(survey_response: pd.Series):
        return Participant(first_name=survey_response[0],
                           last_name=survey_response[1],
                           address=survey_response[2])

