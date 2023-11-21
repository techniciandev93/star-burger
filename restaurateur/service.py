import requests
from geopy import distance

from star_burger.settings import YANDEX_GEOCODER_TOKEN


class FetchCoordinatesError(TypeError):
    pass


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def calculate_distance(first_address, second_address, apikey=YANDEX_GEOCODER_TOKEN):
    first_fetch_coordinates = fetch_coordinates(apikey, first_address)
    second_fetch_coordinates = fetch_coordinates(apikey, second_address)
    if not any([first_fetch_coordinates, second_fetch_coordinates]):
        raise FetchCoordinatesError('Одна из координат или обе координаты не определенны')
    return distance.distance(fetch_coordinates(apikey, first_address),
                             fetch_coordinates(apikey, second_address)).km
