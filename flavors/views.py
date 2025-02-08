from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUser
from flavors.models import Flavor, FlavorGroup
from flavors.serializers import (
    FlavorDetailSerializer,
    FlavorGroupSerializer,
    FlavorGroupSummarySerializer,
    FlavorSerializer,
    FlavorSummarySerializer,
)


class FlavorGroupViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    model = FlavorGroup
    queryset = model.objects.all()
    http_method_names = ["post", "get"]
    permission_classes = [IsSystemAdminUser]
    autocomplete_fields = ["id", "name"]

    def get_serializer_class(self):
        if self.action == "list":
            return FlavorGroupSummarySerializer
        return FlavorGroupSerializer


class FlavorViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["post", "get"]
    model = Flavor
    queryset = model.objects.all()
    permission_classes = [IsSystemAdminUser]
    autocomplete_fields = ["id", "name"]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["flavor_group__name", "name"]
    ordering = ["flavor_group__name", "name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlavorDetailSerializer
        elif self.action == "list":
            return FlavorSummarySerializer
        return FlavorSerializer
