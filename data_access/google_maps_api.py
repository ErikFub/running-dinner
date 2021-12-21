import requests
from env.credentials_manager import CredentialsManager


class GoogleMapsAPI:
    def __init__(self):
        self.base_url = "https://maps.googleapis.com/maps/api/directions/"
        self.data_format = "json"
        self.api_key = CredentialsManager.get_password('directions_api')

    def get_distance(self, node, neighbor, mode: str = "transit"):
        response = requests.get(self.base_url + self.data_format, params={'origin': node,
                                                                          'destination': neighbor,
                                                                          'key': self.api_key,
                                                                          'mode': mode,
                                                                          'units': 'metric'})
        response = response.json()
        return response['routes'][0]['legs'][0]['duration']['value']
