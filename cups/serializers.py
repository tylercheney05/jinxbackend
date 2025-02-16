from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from cups.models import Cup


def get_size(obj):
    return {"value": obj.size, "display": obj.get_size_display()}


class CupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cup
        fields = ["id", "size", "price", "conversion_factor"]
        read_only_fields = ["id"]


class CupSummarySerializer(ReadOnlyModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = Cup
        fields = [
            "id",
            "size",
        ]

    def get_size(self, obj):
        return get_size(obj)


class CupDetailSerializer(ReadOnlyModelSerializer):
    size = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cup
        fields = ["id", "size", "price", "conversion_factor"]

    def get_size(self, obj):
        return get_size(obj)
