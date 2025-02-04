from rest_framework import serializers

from flavors.models import FlavorGroup


class FlavorGroupSerializer(serializers.ModelSerializer):
    uom__display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlavorGroup
        fields = ["name", "uom", "uom__display", "price"]

    def get_uom__display(self, obj):
        return obj.get_uom_display()


class FlavorGroupDetailSerializer(serializers.ModelSerializer):
    uom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FlavorGroup
        fields = ["id", "uom"]
        read_only_fields = ["id", "uom"]

    def get_uom(self, obj):
        return {
            "value": obj.uom,
            "display": obj.get_uom_display(),
        }
