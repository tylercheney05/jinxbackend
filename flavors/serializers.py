from rest_framework import serializers

from flavors.models import Flavor, FlavorGroup


class FlavorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlavorGroup
        fields = ["name", "uom"]


class FlavorSerializer(serializers.ModelSerializer):
    flavor_group__uom__display = serializers.SerializerMethodField()
    flavor_group__name = serializers.CharField(
        source="flavor_group.name", read_only=True
    )

    class Meta:
        model = Flavor
        fields = [
            "name",
            "flavor_group",
            "flavor_group__uom__display",
            "flavor_group__name",
        ]

    def get_flavor_group__uom__display(self, obj):
        return obj.flavor_group.get_uom_display()
