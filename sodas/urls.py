from rest_framework import routers
from sodas.views import SodaViewSet

router = routers.DefaultRouter()
router.register('', SodaViewSet, basename='sodas')
urlpatterns = router.urls