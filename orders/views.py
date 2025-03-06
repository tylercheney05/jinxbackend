import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import AutocompleteViewSetMixin
from orders.models import (
    Discount,
    Order,
    OrderDiscount,
    OrderItem,
    OrderName,
    OrderPaidAmount,
)
from orders.serializers import (
    DiscountSerializer,
    OrderDetailSerializer,
    OrderItemSerializer,
    OrderNameSerializer,
    OrderSerializer,
)
from orders.utils import get_price


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
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_paid", "collected_by", "location", "is_complete"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=["patch"], url_path="complete-order-payment")
    def complete_order_payment(self, request, *args, **kwargs):
        order_name_id = request.data.get("order_name")
        paid_amount = request.data.get("paid_amount")
        discount_id = request.data.get("discount", 0)

        obj = self.get_object()
        obj.is_paid = True
        obj.order_name_id = order_name_id
        obj.save()

        OrderPaidAmount.objects.create(order=obj, paid_amount=paid_amount)

        if discount_id:
            OrderDiscount.objects.create(order=obj, discount_id=discount_id)
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=["patch"], url_path="update-in-progress")
    def update_in_progress(self, request, *args, **kwargs):
        obj = self.get_object()
        is_in_progress = request.data.get("is_in_progress", False)
        is_complete = request.data.get("is_complete", False)
        obj.is_in_progress = is_in_progress
        obj.is_complete = is_complete
        obj.save()
        return Response(self.get_serializer(obj).data)

    @action(detail=False, methods=["get"], url_path="pending")
    def pending_orders(self, request, *args, **kwargs):
        location_id = int(request.query_params.get("location_id", "0"))
        queryset = Order.objects.pending_orders(location_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderItemViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    http_method_names = ["post", "get", "patch", "delete"]
    queryset = OrderItem.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["order__is_paid", "order__collected_by", "order"]

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


class OrderNameViewSet(
    AutocompleteViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = OrderName.objects.all()
    permission_classes = [permissions.IsAdminUser]
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
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DiscountSerializer
    autocomplete_fields = ["id", "name"]
