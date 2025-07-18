from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import FlavorGroup


class FlavorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlavorGroup
        fields = ["name", "uom", "price"]


class FlavorGroupSerializerReadOnly(ReadOnlyModelSerializer):
    uom = serializers.SerializerMethodField()

    class Meta:
        model = FlavorGroup
        fields = ["id", "name", "uom", "price"]

    def get_uom(self, obj: FlavorGroup):
        return {"value": obj.uom, "display": obj.get_uom_display()}
