from django.apps import apps
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from orders.models import Discount, Order, OrderName, OrderPaidAmount
from orders.serializers import (
    DiscountSerializer,
    OrderDetailSerializer,
    OrderNameSerializer,
    OrderPaidAmountSerializer,
    OrderSerializer,
)
from orders.utils.discount import calculate_order_price_with_discount


class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    http_method_names = ["get", "patch", "delete"]
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "is_paid", "collected_by", "location", "is_complete"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    @action(detail=True, methods=["patch"], url_path="update-in-progress")
    def update_in_progress(self, request, *args, **kwargs):
        obj = self.get_object()
        is_in_progress = request.data.get("is_in_progress", False)
        is_complete = request.data.get("is_complete", False)
        obj.is_in_progress = is_in_progress
        obj.is_complete = is_complete
        obj.save()
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=["get"], url_path="price")
    def price(self, request, *args, **kwargs):
        obj = self.get_object()
        price = 0

        discount_id = int(request.query_params.get("discount", 0))
        discount_model = apps.get_model("orders.Discount")
        discount = discount_model.objects.get(id=discount_id) if discount_id else None

        price = calculate_order_price_with_discount(obj, discount)
        return Response({"data": price}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="pending")
    def pending_orders(self, request, *args, **kwargs):
        location_id = int(request.query_params.get("location_id", "0"))
        queryset = Order.objects.pending_orders(location_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderNameViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    http_method_names = ["post", "get", "put", "delete"]
    queryset = OrderName.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = OrderNameSerializer
    autocomplete_fields = ["id", "name"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ["name"]
    ordering_fields = ["name"]


class DiscountViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = Discount.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = DiscountSerializer
    autocomplete_fields = ["id", "name"]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class OrderPaidAmountViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    http_method_names = ["post"]
    model = OrderPaidAmount
    queryset = model.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderPaidAmountSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
