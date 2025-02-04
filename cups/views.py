import pandas as pd
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from cups.models import Cup
from cups.serializers import CupDetailSerializer, CupSerializer


class CupViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["get", "post"]
    queryset = Cup.objects.all()
    serializer_class = CupSerializer
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CupDetailSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], url_path="autocomplete")
    def autocomplete(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        df = pd.DataFrame(
            queryset.annotate(
                size__display=Concat(F("size"), Value(" oz"), output_field=CharField())
            ).values("id", "size__display")
        )
        return Response({"results": df.to_dict("records")})
