from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from sodas.models import Soda
from sodas.serializers import SodaSerializer


class SodaViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    http_method_names = ["get", "post"]
    queryset = Soda.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = SodaSerializer
    autocomplete_fields = ["id", "name"]
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["name"]
    ordering = ["name"]
