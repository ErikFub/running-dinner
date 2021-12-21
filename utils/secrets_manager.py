import os


class SecretsManager:
    @staticmethod
    def get_password(application: str):
        application_mapping = {'directions_api': 'directions_api_key'}
        return os.getenv(application_mapping[application])
