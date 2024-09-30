from rest_framework import routers

from menuitems.views import LimitedTimePromotionViewSet, MenuItemViewSet

router = routers.DefaultRouter()
router.register(
    "limited-time-promotions",
    LimitedTimePromotionViewSet,
    basename="limited-time-promotions",
)
router.register("", MenuItemViewSet, basename="menu-items")
urlpatterns = router.urls
