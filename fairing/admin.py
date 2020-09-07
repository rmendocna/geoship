from django.contrib import admin

from .models import Ship, ShipPosition


@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = ['name', 'imo', 'flag', 'build', 'ship_type']


@admin.register(ShipPosition)
class ShipPositionAdmin(admin.ModelAdmin):
    list_display = ['ship', 'timestamp', 'latitude', 'longitude']
