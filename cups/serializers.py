from rest_framework import serializers

from cups.models import Cup


class CupSerializer(serializers.ModelSerializer):
    size__display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cup
        fields = ["id", "size", "size__display", "price", "conversion_factor"]
        read_only_fields = ["id"]

    def get_size__display(self, obj):
        return obj.get_size_display()


class CupDetailSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cup
        fields = ["id", "size", "price", "conversion_factor"]
        read_only_fields = ["id"]

    def get_size(self, obj):
        return {"value": obj.size, "display": obj.get_size_display()}
