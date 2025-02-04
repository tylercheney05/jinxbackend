from rest_framework import serializers

from flavors.serializers import FlavorDetailSerializer
from orders.models import CustomOrderFlavor


class CustomOrderFlavorSerializer(serializers.ModelSerializer):
    flavor = FlavorDetailSerializer(read_only=True)

    class Meta:
        model = CustomOrderFlavor
        fields = ["id", "quantity", "flavor"]
        read_only_fields = ["id", "quantity"]
