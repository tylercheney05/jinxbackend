from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import Flavor
from flavors.serializers.flavor_group import FlavorGroupSerializerReadOnly


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = [
            "name",
            "flavor_group",
            "sugar_free_available",
        ]


class FlavorSerializerReadOnly(ReadOnlyModelSerializer):
    flavor_group = FlavorGroupSerializerReadOnly()

    class Meta:
        model = Flavor
        fields = [
            "id",
            "name",
            "flavor_group",
            "sugar_free_available",
        ]
