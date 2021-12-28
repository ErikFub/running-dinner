import requests
from utils.secrets_manager import SecretsManager


class DirectionsAPI:
    def __init__(self, origin, destination, mode):
        self.base_url = "https://maps.googleapis.com/maps/api/directions/"
        self.data_format = "json"
        self.api_key = SecretsManager.get_password('directions_api')
        self.response = self._get_response(origin, destination, mode)
        self.distance = self._get_distance()
        self.polyline = self._get_polyline()

    def _get_response(self, origin, destination, mode):
        response = requests.get(self.base_url + self.data_format, params={'origin': origin + ' Lisbon',
                                                                          'destination': destination + ' Lisbon',
                                                                          'key': self.api_key,
                                                                          'mode': mode,
                                                                          'units': 'metric'})
        return response.json()

    def _get_distance(self):
        return self.response['routes'][0]['legs'][0]['duration']['value']

    def _get_polyline(self):
        return self.response['routes'][0]['overview_polyline']['points']
