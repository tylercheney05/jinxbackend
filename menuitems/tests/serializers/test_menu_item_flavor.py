from django.test import TestCase
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.serializers import FlavorDetailSerializer, FlavorSummarySerializer
from menuitems.models import MenuItemFlavor
from menuitems.serializers.menu_item_flavor import (
    MenuItemFlavorDetailSerializer,
    MenuItemFlavorSerializer,
    MenuItemFlavorSummarySerializer,
)


class TestMenuItemFlavorSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(MenuItemFlavorSerializer, serializers.ModelSerializer)
        )

    def test_model(self):
        serializer = MenuItemFlavorSerializer()
        self.assertEqual(serializer.Meta.model, MenuItemFlavor)

    def test_fields(self):
        serializer = MenuItemFlavorSerializer()
        self.assertEqual(
            serializer.Meta.fields, ["id", "menu_item", "flavor", "quantity"]
        )


class TestMenuItemFlavorDetailSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(MenuItemFlavorDetailSerializer, ReadOnlyModelSerializer)
        )
        self.assertTrue(
            issubclass(MenuItemFlavorDetailSerializer, serializers.ModelSerializer)
        )

    def test_flavor(self):
        serializer = MenuItemFlavorDetailSerializer()
        self.assertIsInstance(serializer.fields["flavor"], FlavorDetailSerializer)

    def test_model(self):
        serializer = MenuItemFlavorDetailSerializer()
        self.assertEqual(serializer.Meta.model, MenuItemFlavor)

    def test_fields(self):
        serializer = MenuItemFlavorDetailSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "flavor", "quantity"])


class TestMenuItemFlavorSummarySerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(MenuItemFlavorSummarySerializer, ReadOnlyModelSerializer)
        )
        self.assertTrue(
            issubclass(MenuItemFlavorSummarySerializer, serializers.ModelSerializer)
        )

    def test_flavor(self):
        serializer = MenuItemFlavorSummarySerializer()
        self.assertIsInstance(serializer.fields["flavor"], FlavorSummarySerializer)

    def test_model(self):
        serializer = MenuItemFlavorSummarySerializer()
        self.assertEqual(serializer.Meta.model, MenuItemFlavor)

    def test_fields(self):
        serializer = MenuItemFlavorSummarySerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "flavor", "quantity"])
