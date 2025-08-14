from django.test import TestCase
from rest_framework import serializers

from menuitems.models import MenuItemPrice
from menuitems.serializers.menu_item_price import MenuItemPriceSerializer


class TestMenuItemPriceSerializer(TestCase):
    def test_sub_class(self):
        assert issubclass(MenuItemPriceSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = MenuItemPriceSerializer()
        self.assertEqual(serializer.Meta.model, MenuItemPrice)

    def test_fields(self):
        serializer = MenuItemPriceSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "price"])
