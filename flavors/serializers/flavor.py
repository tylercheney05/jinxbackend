from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import Flavor
from flavors.serializers import (
    FlavorGroupDetailSerializer,
    FlavorGroupSummarySerializer,
)


class FlavorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flavor
        fields = [
            "id",
            "name",
            "flavor_group",
            "sugar_free_available",
        ]
        read_only_fields = ["id"]


class FlavorDetailSerializer(ReadOnlyModelSerializer):
    flavor_group = FlavorGroupDetailSerializer()

    class Meta:
        model = Flavor
        fields = ["id", "name", "flavor_group", "sugar_free_available"]


class FlavorSummarySerializer(ReadOnlyModelSerializer):
    flavor_group = FlavorGroupSummarySerializer()

    class Meta:
        model = Flavor
        fields = ["id", "name", "flavor_group"]
