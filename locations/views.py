from rest_framework import mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from locations.models import Location
from locations.serializers import LocationSerializer


class LocationViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = Location.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = LocationSerializer
    autocomplete_fields = ["id", "name"]
