import json

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import OrderItem
from orders.serializers import OrderItemSerializer
from orders.utils.order_item import get_price


class OrderItemViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    http_method_names = ["post", "get", "patch", "delete"]
    queryset = OrderItem.objects.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    serializer_class = OrderItemSerializer
    filterset_fields = ["order__is_paid", "order__collected_by", "order"]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="price")
    def price(self, request, *args, **kwargs):
        cup_id = int(request.query_params.get("cup", "0"))
        menu_item_id = (
            int(request.query_params.get("menu_item", "0"))
            if request.query_params.get("menu_item")
            else None
        )
        custom_order__soda_id = (
            int(request.query_params.get("custom_order__soda", "0"))
            if request.query_params.get("custom_order__soda", None)
            else None
        )
        custom_order_flavor_ids = (
            json.loads(request.query_params.get("custom_order_flavors", "[]"))
            if request.query_params.get("custom_order_flavors", None)
            else []
        )
        return Response(
            {
                "price": get_price(
                    cup_id, menu_item_id, custom_order__soda_id, custom_order_flavor_ids
                )
            },
            status=status.HTTP_200_OK,
        )
