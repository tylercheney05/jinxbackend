from rest_framework import serializers

from flavors.models import Flavor
from flavors.serializers import FlavorGroupDetailSerializer


class FlavorSerializer(serializers.ModelSerializer):
    flavor_group__uom__display = serializers.SerializerMethodField()
    flavor_group__name = serializers.CharField(
        source="flavor_group.name", read_only=True
    )
    flavor_group__price = serializers.CharField(
        source="flavor_group.price", read_only=True
    )

    class Meta:
        model = Flavor
        fields = [
            "id",
            "name",
            "flavor_group",
            "flavor_group__uom__display",
            "flavor_group__name",
            "flavor_group__price",
            "sugar_free_available",
        ]
        read_only_fields = ["id"]

    def get_flavor_group__uom__display(self, obj):
        return obj.flavor_group.get_uom_display()


class FlavorDetailSerializer(serializers.ModelSerializer):
    flavor_group = FlavorGroupDetailSerializer(read_only=True)

    class Meta:
        model = Flavor
        fields = ["id", "name", "flavor_group", "sugar_free_available"]
        read_only_fields = ["id", "name", "sugar_free_available"]
