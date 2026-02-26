from rest_framework import serializers

from locations.models import DeviceToken, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "name",
        ]


class DeviceAuthResponseSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(source="location.id")
    location_name = serializers.CharField(source="location.name")

    class Meta:
        model = DeviceToken
        fields = [
            "token",
            "name",
            "location_id",
            "location_name",
        ]
