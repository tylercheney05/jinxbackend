from rest_framework import serializers

from orders.models import OrderDiscount


class OrderDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDiscount
        fields = ["order", "discount"]
        write_only_fields = ["order"]
