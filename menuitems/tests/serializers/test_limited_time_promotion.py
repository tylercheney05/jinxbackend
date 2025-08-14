from django.test import TestCase
from rest_framework import serializers

from menuitems.models import LimitedTimePromotion
from menuitems.serializers.limited_time_promotion import LimitedTimePromotionSerializer


class TestLimitedTimePromotionSerializer(TestCase):
    def test_sub_class(self):
        assert issubclass(LimitedTimePromotionSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = LimitedTimePromotionSerializer()
        self.assertEqual(serializer.Meta.model, LimitedTimePromotion)

    def test_fields(self):
        serializer = LimitedTimePromotionSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "name", "is_archived"])
