import pandas as pd


class FinalDestination:
    def __init__(self):
        self.name, self.address = self.get_dummy()

    def get(self):
        pass

    @staticmethod
    def get_dummy():
        data = pd.read_csv("sample_data/final_destination_sample.csv")
        return data.iloc[0]['name'], data.iloc[0]['address']
