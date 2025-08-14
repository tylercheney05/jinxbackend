from django.test import TestCase
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.serializers.flavor import FlavorSerializerReadOnly
from menuitems.models import MenuItemFlavor
from menuitems.serializers.menu_item_flavor import (
    MenuItemFlavorSerializer,
    MenuItemFlavorSerializerReadOnly,
)


class TestMenuItemFlavorSerializer(TestCase):
    def test_sub_classes(self):
        assert issubclass(MenuItemFlavorSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = MenuItemFlavorSerializer()
        self.assertEqual(serializer.Meta.model, MenuItemFlavor)

    def test_fields(self):
        serializer = MenuItemFlavorSerializer()
        self.assertEqual(serializer.Meta.fields, ["quantity", "flavor"])


class TestMenuItemFlavorSerializerReadOnly(TestCase):
    def test_sub_classes(self):
        assert issubclass(MenuItemFlavorSerializerReadOnly, serializers.ModelSerializer)
        assert issubclass(MenuItemFlavorSerializerReadOnly, ReadOnlyModelSerializer)

    def test_model(self):
        serializer = MenuItemFlavorSerializerReadOnly()
        self.assertEqual(serializer.Meta.model, MenuItemFlavor)

    def test_fields(self):
        serializer = MenuItemFlavorSerializerReadOnly()
        self.assertEqual(serializer.Meta.fields, ["quantity", "flavor"])

    def test_flavor(self):
        serializer = MenuItemFlavorSerializerReadOnly()
        self.assertIsInstance(serializer.fields["flavor"], FlavorSerializerReadOnly)
