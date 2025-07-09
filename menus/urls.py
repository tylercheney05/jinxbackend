from rest_framework import routers

from menus.views import MenuViewSet

router = routers.DefaultRouter()
router.register("", MenuViewSet, basename="menus")
urlpatterns = router.urls
