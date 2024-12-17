import requests


class APIClient:
    _instance = None

    BASE_URL = "https://baymanap.pythonanywhere.com/cinema"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls)
        return cls._instance

    def get(self, endpoint, **kwargs):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise e

    def post(self, endpoint, json=None, **kwargs):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, json=json, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise e
