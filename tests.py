import json

from fastapi.testclient import TestClient
from main import app
from config import *
import requests
import os


client = TestClient(app)


def test_read_main():

    headers = {YANDEX_API_KEY: os.environ.get('YANDEX_KEY')}
    lat = 43.112321
    lon = 41.12312
    coordinates = {'lat': lat, 'lon': lon}
    response = requests.get(URL, params=coordinates, headers=headers)
    fact = json.loads(response.content)["fact"]

    response = client.get("/weather")
    assert response.status_code == 422

    response = client.get("")
    assert response.status_code == 404

    response = client.get(f"/weather?lat=1asd23123&lon=123132asda")
    assert response.status_code == 422

    response = client.get(f"/weather?lat={lat}&lon={lon}")
    assert response.status_code == 200
    assert response.json() == {key: fact[key] for key in WEATHER_FAST_KEYS}

