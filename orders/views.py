from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import AutocompleteViewSetMixin
from orders.models import Order, OrderItem, OrderName
from orders.serializers import OrderItemSerializer, OrderNameSerializer, OrderSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    http_method_names = ["get", "patch"]
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_paid", "collected_by", "location", "is_prepared"]

    @action(detail=True, methods=["patch"], url_path="complete-order-payment")
    def complete_order_payment(self, request, *args, **kwargs):
        order_name_id = request.data.get("order_name")

        obj = self.get_object()
        obj.is_paid = True
        obj.order_name_id = order_name_id
        obj.save()
        return Response(self.get_serializer(obj).data)


class OrderItemViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = OrderItem.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["order__is_paid", "order__collected_by"]


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
