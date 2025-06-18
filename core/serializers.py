from rest_framework import serializers


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    """
    Use this serializer for Public serializers, where the data is limited and read only.
    """

    def create(self, validated_data):
        raise serializers.ValidationError(
            "Read-only serializer does not have write access"
        )

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            "Read-only serializer does not have write access"
        )
