import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from config import *
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


class ForeignApiError(HTTPException):
    def __init__(self, api_name, status_code):
        super().__init__(status_code=403, detail=f'Ошибка {api_name}. Код {status_code}')


@app.get("/weather", response_class=JSONResponse)
def weather(lat: float, lon: float):
    headers = {YANDEX_API_KEY: os.environ.get('YANDEX_KEY')}
    coordinates = {'lat': lat, 'lon': lon}
    response = requests.get(URL, params=coordinates, headers=headers)
    if response.status_code != 200:
        raise ForeignApiError('Yandex', response.status_code)
    fact = json.loads(response.content)["fact"]
    return {key: fact[key] for key in WEATHER_FAST_KEYS}
