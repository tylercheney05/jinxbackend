from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
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


class OrderViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    http_method_names = ["get", "patch"]
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
        obj.is_in_progress = is_in_progress

        if not is_in_progress:
            obj.items.all().update(is_prepared=False)
        obj.save()
        return Response(self.get_serializer(obj).data)


class OrderItemViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get", "patch"]
    queryset = OrderItem.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["order__is_paid", "order__collected_by", "order"]

    @action(detail=True, methods=["patch"], url_path="prepare-order-item")
    def prepare_order_item(self, request, *args, **kwargs):
        obj = self.get_object()
        is_prepared = request.data.get("is_prepared", False)
        obj.is_prepared = is_prepared
        obj.save()

        remaining_order_items = obj.order.items.filter(is_prepared=False)
        if not remaining_order_items.exists():
            obj.order.is_complete = True
            obj.order.is_in_progress = False
            obj.order.save()
        return Response(OrderDetailSerializer(obj.order).data)


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
