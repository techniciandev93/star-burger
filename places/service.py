from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from foodcartapp.models import Restaurant, Order
from restaurateur.service import fetch_coordinates
from .models import Place

from star_burger.settings import YANDEX_GEOCODER_TOKEN


def create_places(addresses):
    places = []
    for address in addresses:
        coordinate = fetch_coordinates(YANDEX_GEOCODER_TOKEN, address)
        if coordinate:
            lng, lat = coordinate
        else:
            lng, lat = None, None
        places.append(Place(address=address, lng=lng, lat=lat, date=timezone.now()))
    Place.objects.bulk_create(places, batch_size=1000)
    return places


def get_existing_places(orders):
    addresses = []
    for order in orders:
        addresses.append(order.address)
        for restaurant in order.restaurants:
            addresses.append(restaurant.address)

    existing_places = Place.objects.filter(address__in=addresses)
    missing_addresses = list(set(addresses) - set(existing_places.values_list('address', flat=True)))
    if missing_addresses:
        created_places = create_places(missing_addresses)
        existing_places = list(existing_places)
        existing_places.extend(created_places)
    places = {place.address: (place.lng, place.lat) for place in existing_places}
    return places


@receiver(post_save, sender=Restaurant)
@receiver(post_save, sender=Order)
def update_place_coordinates(sender, instance, **kwargs):
    coordinates = fetch_coordinates(YANDEX_GEOCODER_TOKEN, instance.address)
    if coordinates:
        lng, lat = coordinates
    else:
        lng, lat = None, None
    Place.objects.get_or_create(address=instance.address,
                                defaults={
                                    'date': timezone.now(),
                                    'lng': lng,
                                    'lat': lat}
                                )
