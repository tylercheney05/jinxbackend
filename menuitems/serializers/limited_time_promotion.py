from rest_framework import serializers

from menuitems.models import LimitedTimePromotion


class LimitedTimePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitedTimePromotion
        fields = ["id", "name", "is_archived"]
        read_only_fields = ["id"]
