from rest_framework import mixins, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from locations.models import DeviceToken, Location
from locations.serializers import DeviceAuthResponseSerializer, LocationSerializer


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


class DeviceAuthView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            device = DeviceToken.objects.select_related("location").get(
                token=token, is_active=True
            )
        except DeviceToken.DoesNotExist:
            return Response(
                {"error": "Invalid or inactive device token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = DeviceAuthResponseSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
