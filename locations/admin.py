from django.contrib import admin

from locations.models import DeviceToken, Location

admin.site.register(Location)
admin.site.register(DeviceToken)
