from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from core.viewsets import AutocompleteViewSetMixin
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
