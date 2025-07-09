from rest_framework import serializers

from menus.models import Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",
            "version",
            "date",
        ]
        read_only_fields = ["id"]
