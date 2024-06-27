from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response

from core.permissions import IsSystemAdminUser
from menuitems.models import MenuItem
from menuitems.serializers import MenuItemSerializer


class MenuItemViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = MenuItem.objects.all()
    permission_classes = [IsSystemAdminUser]
    serializer_class = MenuItemSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["soda__name"]
    ordering = ["soda__name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
