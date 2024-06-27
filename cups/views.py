from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUser
from cups.models import Cup
from cups.serializers import CupSerializer


class CupViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    http_method_names = ["get", "post"]
    queryset = Cup.objects.all()
    permission_classes = [IsSystemAdminUser]
    serializer_class = CupSerializer
