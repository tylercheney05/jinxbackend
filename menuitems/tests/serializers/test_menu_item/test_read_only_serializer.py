from django.test import TestCase
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from menuitems.models import MenuItem
from menuitems.serializers.menu_item import MenuItemSerializerReadOnly
from menuitems.serializers.menu_item_flavor import MenuItemFlavorSerializerReadOnly
from sodas.serializers import SodaSerializer


class TestMenuItemSerializerReadOnly(TestCase):
    def test_sub_class(self):
        assert issubclass(MenuItemSerializerReadOnly, ReadOnlyModelSerializer)
        assert issubclass(MenuItemSerializerReadOnly, serializers.ModelSerializer)

    def test_model(self):
        serializer = MenuItemSerializerReadOnly()
        self.assertEqual(serializer.Meta.model, MenuItem)

    def test_fields(self):
        serializer = MenuItemSerializerReadOnly()
        expected_fields = ["id", "name", "soda", "flavors", "cup_prices"]
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_soda(self):
        serializer = MenuItemSerializerReadOnly()
        self.assertIsInstance(serializer.fields["soda"], SodaSerializer)

    def test_flavors(self):
        serializer = MenuItemSerializerReadOnly()
        self.assertIsInstance(
            serializer.fields["flavors"].child, MenuItemFlavorSerializerReadOnly
        )
        self.assertTrue(serializer.fields["flavors"].many)
