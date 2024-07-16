from rest_framework import routers

from orders.views import OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("items", OrderItemViewSet, basename="order-items")
router.register("", OrderViewSet, basename="orders")
urlpatterns = router.urls
