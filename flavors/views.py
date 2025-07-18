from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUser
from flavors.models import Flavor, FlavorGroup
from flavors.serializers import FlavorGroupSerializer, FlavorSerializer


class FlavorGroupViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    http_method_names = ["post", "get", "put"]
    queryset = FlavorGroup.objects.all()
    permission_classes = [IsSystemAdminUser]
    serializer_class = FlavorGroupSerializer
    autocomplete_fields = ["id", "name"]


class FlavorViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = Flavor.objects.all()
    permission_classes = [IsSystemAdminUser]
    serializer_class = FlavorSerializer
    autocomplete_fields = ["id", "name"]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["flavor_group__name", "name"]
    ordering = ["flavor_group__name", "name"]
