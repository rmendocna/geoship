from django.http import JsonResponse
from django.shortcuts import render


from .models import Ship, ShipPosition


def api_ship_list(request):

    ships = Ship.objects.values('imo', 'name', 'flag', 'ship_type')
    return JsonResponse(ships, safe=False)


def api_ship_position_list(request, imo):

    ship = Ship.objects.get(imo=imo)
    positions = ShipPosition.objects.filter(ship=ship).order_by('-timestamp').values()
    return JsonResponse(positions, safe=False)
