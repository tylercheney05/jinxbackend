from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from cups.models import Cup


class CupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cup
        fields = ["id", "size", "price", "conversion_factor"]


class CupSerializerReadOnly(ReadOnlyModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = Cup
        fields = ["id", "size", "price", "conversion_factor"]

    def get_size(self, obj: Cup):
        return {"value": obj.size, "display": obj.get_size_display()}
