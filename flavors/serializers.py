from rest_framework import serializers

from flavors.models import Flavor, FlavorGroup


class FlavorGroupSerializer(serializers.ModelSerializer):
    uom__display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlavorGroup
        fields = ["name", "uom", "uom__display", "price"]

    def get_uom__display(self, obj):
        return obj.get_uom_display()


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
        ]
        read_only_fields = ["id"]

    def get_flavor_group__uom__display(self, obj):
        return obj.flavor_group.get_uom_display()
