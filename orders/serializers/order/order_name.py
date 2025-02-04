from rest_framework import serializers

from orders.models import OrderName


class OrderNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderName
        fields = ["id", "name"]
        read_only_fields = ["id"]
