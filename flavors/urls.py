from rest_framework import routers
from flavors.views import FlavorViewSet

router = routers.DefaultRouter()
router.register('', FlavorViewSet, basename='flavors')
urlpatterns = router.urls