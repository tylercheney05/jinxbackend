from rest_framework import routers

from flavors.views import FlavorGroupViewSet, FlavorViewSet

router = routers.DefaultRouter()
router.register("groups", FlavorGroupViewSet, basename="flavor-groups")
router.register("", FlavorViewSet, basename="flavors")
urlpatterns = router.urls
