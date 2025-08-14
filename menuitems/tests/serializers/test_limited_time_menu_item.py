from django.test import TestCase
from rest_framework import serializers

from menuitems.models import LimitedTimeMenuItem
from menuitems.serializers.limited_time_menu_item import LimitedTimeMenuItemSerializer


class TestLimitedTimePromotionSerializer(TestCase):
    def test_sub_class(self):
        assert issubclass(LimitedTimeMenuItemSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = LimitedTimeMenuItemSerializer()
        self.assertEqual(serializer.Meta.model, LimitedTimeMenuItem)

    def test_fields(self):
        serializer = LimitedTimeMenuItemSerializer()
        self.assertEqual(serializer.Meta.fields, ["limited_time_promo"])
