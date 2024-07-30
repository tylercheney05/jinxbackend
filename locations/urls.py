from rest_framework import routers

from locations.views import LocationViewSet

router = routers.DefaultRouter()
router.register("", LocationViewSet, basename="locations")
urlpatterns = router.urls
