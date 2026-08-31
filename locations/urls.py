from django.urls import path
from rest_framework import routers

from locations.views import DeviceAuthView, LocationViewSet

router = routers.DefaultRouter()
router.register("", LocationViewSet, basename="locations")
urlpatterns = [
    path("device-auth/", DeviceAuthView.as_view(), name="device-auth"),
] + router.urls
