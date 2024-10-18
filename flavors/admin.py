from django.contrib import admin

from flavors.models import Flavor, FlavorGroup

admin.site.register(Flavor)
admin.site.register(FlavorGroup)
