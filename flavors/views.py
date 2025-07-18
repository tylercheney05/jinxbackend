from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUser
from flavors.models import Flavor, FlavorGroup
from flavors.serializers.flavor import FlavorSerializer, FlavorSerializerReadOnly
from flavors.serializers.flavor_group import (
    FlavorGroupSerializer,
    FlavorGroupSerializerReadOnly,
)


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

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return FlavorGroupSerializer
        return FlavorGroupSerializerReadOnly


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

    def get_serializer_class(self):
        if self.action in ["create"]:
            return FlavorSerializer
        return FlavorSerializerReadOnly
