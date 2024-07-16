from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    http_method_names = ["get", "patch"]
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_paid", "completed_by"]

    @action(detail=True, methods=["patch"], url_path="complete-order")
    def complete_order(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_paid = True
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
    filterset_fields = ["order__is_paid", "order__completed_by"]
