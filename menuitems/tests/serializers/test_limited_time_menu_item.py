from django.test import TestCase
from rest_framework import serializers

from menuitems.models import LimitedTimeMenuItem
from menuitems.serializers.limited_time_menu_item import LimitedTimeMenuItemSerializer


class TestLimitedTimeMenuItemSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(LimitedTimeMenuItemSerializer, serializers.ModelSerializer)
        )

    def test_model(self):
        serializer = LimitedTimeMenuItemSerializer()
        self.assertEqual(serializer.Meta.model, LimitedTimeMenuItem)

    def test_fields(self):
        serializer = LimitedTimeMenuItemSerializer()
        self.assertEqual(
            serializer.Meta.fields,
            ["menu_item", "limited_time_promo"],
        )
