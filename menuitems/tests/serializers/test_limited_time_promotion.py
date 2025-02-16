from django.test import TestCase
from model_bakery import baker

from menuitems.models import LimitedTimePromotion
from menuitems.serializers.limited_time_promotion import LimitedTimePromotionSerializer


class TestLimitedTimePromotionSerializer(TestCase):
    def test_model(self):
        serializer = LimitedTimePromotionSerializer()
        self.assertEqual(serializer.Meta.model, LimitedTimePromotion)

    def test_fields(self):
        serializer = LimitedTimePromotionSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "name", "is_archived"])

    def test_read_only_fields(self):
        serializer = LimitedTimePromotionSerializer()
        self.assertEqual(serializer.Meta.read_only_fields, ["id"])
