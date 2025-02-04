from rest_framework import routers

from orders.views import (
    DiscountViewSet,
    OrderItemViewSet,
    OrderNameViewSet,
    OrderPaidAmountViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register("paid-amounts", OrderPaidAmountViewSet, basename="paid-amounts")
router.register("discounts", DiscountViewSet, basename="discounts")
router.register("items", OrderItemViewSet, basename="order-items")
router.register("order-names", OrderNameViewSet, basename="order-names")
router.register("", OrderViewSet, basename="orders")
urlpatterns = router.urls
