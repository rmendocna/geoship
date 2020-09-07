from django.http import Http404, JsonResponse

from .models import Ship, ShipPosition


def api_ship_list(request):

    ships = Ship.objects.values('imo', 'name', 'flag', 'ship_type')
    return JsonResponse(list(ships), safe=False)


def api_ship_position_list(request, imo):

    try:
        ship = Ship.objects.get(imo=imo)
    except Ship.DoesNotExist:
        raise Http404('Could not find IMO')

    positions = ShipPosition.objects.filter(ship=ship).order_by(
        '-timestamp').values('timestamp', 'latitude', 'longitude')
    return JsonResponse(list(positions), safe=False)
