from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import FlavorGroup


class FlavorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlavorGroup
        fields = ["name", "uom", "price"]


class FlavorGroupSummarySerializer(ReadOnlyModelSerializer):
    uom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlavorGroup
        fields = [
            "id",
            "name",
            "uom",
            "price",
        ]

    def get_uom(self, obj):
        return {
            "value": obj.uom,
            "display": obj.get_uom_display(),
        }


class FlavorGroupDetailSerializer(ReadOnlyModelSerializer):
    uom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlavorGroup
        fields = ["id", "uom"]

    def get_uom(self, obj):
        return {
            "value": obj.uom,
            "display": obj.get_uom_display(),
        }
