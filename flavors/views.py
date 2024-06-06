from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUser
from flavors.models import Flavor
from flavors.serializers import FlavorSerializer


class FlavorViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = Flavor.objects.all()
    permission_classes = [IsSystemAdminUser]
    serializer_class = FlavorSerializer
