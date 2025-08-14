from rest_framework import serializers

from menuitems.models import LimitedTimeMenuItem


class LimitedTimeMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitedTimeMenuItem
        fields = ["limited_time_promo"]
