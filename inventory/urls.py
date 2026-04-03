from rest_framework import routers

from inventory.views import InventoryCategoryViewSet, InventoryItemViewSet, InventoryLogViewSet

router = routers.DefaultRouter()
router.register("categories", InventoryCategoryViewSet, basename="inventory-categories")
router.register("items", InventoryItemViewSet, basename="inventory-items")
router.register("logs", InventoryLogViewSet, basename="inventory-logs")
urlpatterns = router.urls
