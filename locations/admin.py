from django.contrib import admin

from locations.models import Device, Location

admin.site.register(Location)
admin.site.register(Device)
