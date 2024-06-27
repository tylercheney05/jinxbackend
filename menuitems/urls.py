from rest_framework import routers

from menuitems.views import MenuItemViewSet

router = routers.DefaultRouter()
router.register("", MenuItemViewSet, basename="menu-items")
urlpatterns = router.urls
