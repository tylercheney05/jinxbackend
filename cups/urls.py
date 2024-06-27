from rest_framework import routers

from cups.views import CupViewSet

router = routers.DefaultRouter()
router.register("", CupViewSet, basename="cups")
urlpatterns = router.urls
