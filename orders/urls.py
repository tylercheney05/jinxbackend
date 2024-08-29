from rest_framework import routers

from orders.views import OrderItemViewSet, OrderNameViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("items", OrderItemViewSet, basename="order-items")
router.register("order-names", OrderNameViewSet, basename="order-names")
router.register("", OrderViewSet, basename="orders")
urlpatterns = router.urls
