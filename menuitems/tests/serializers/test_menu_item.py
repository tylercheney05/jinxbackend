from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from flavors.models import Flavor
from menuitems.models import (
    LimitedTimeMenuItem,
    LimitedTimePromotion,
    MenuItem,
    MenuItemFlavor,
)
from menuitems.serializers.menu_item import (
    AddMenuItemFlavorSerializer,
    MenuItemSerializer,
)
from sodas.models import Soda


class TestAddMenuItemFlavorSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(AddMenuItemFlavorSerializer, serializers.ModelSerializer)
        )

    def test_model(self):
        serializer = AddMenuItemFlavorSerializer()
        self.assertEqual(serializer.Meta.model, MenuItemFlavor)

    def test_fields(self):
        serializer = AddMenuItemFlavorSerializer()
        self.assertEqual(serializer.Meta.fields, ["flavor", "quantity"])


class TestMenuItemSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuItemSerializer, serializers.ModelSerializer))

    def test_menu_item_flavors(self):
        serializer = MenuItemSerializer()
        self.assertIsInstance(
            serializer.fields["menu_item_flavors"],
            serializers.ListField,
        )
        self.assertIsInstance(
            serializer.fields["menu_item_flavors"].child,
            AddMenuItemFlavorSerializer,
        )
        self.assertTrue(serializer.fields["menu_item_flavors"].write_only)

    def test_limited_time_promo(self):
        serializer = MenuItemSerializer()
        self.assertIsInstance(
            serializer.fields["limited_time_promo"],
            serializers.PrimaryKeyRelatedField,
        )
        self.assertQuerySetEqual(
            serializer.fields["limited_time_promo"].queryset,
            LimitedTimePromotion.objects.all(),
        )
        self.assertTrue(serializer.fields["limited_time_promo"].write_only)
        self.assertFalse(serializer.fields["limited_time_promo"].required)
        self.assertTrue(serializer.fields["limited_time_promo"].allow_null)

    def test_model(self):
        serializer = MenuItemSerializer()
        self.assertEqual(serializer.Meta.model, MenuItem)

    def test_fields(self):
        serializer = MenuItemSerializer()
        self.assertEqual(
            serializer.Meta.fields,
            ["id", "name", "soda", "menu_item_flavors", "limited_time_promo"],
        )
        self.assertEqual(serializer.Meta.read_only_fields, ["id"])

    def test_read_only_fields(self):
        serializer = MenuItemSerializer()
        self.assertEqual(serializer.Meta.read_only_fields, ["id"])


class TestMenuItemSerializerValidateMenuItemFlavors(TestCase):
    def test_if_not_value(self):
        serializer = MenuItemSerializer()
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.validate_menu_item_flavors([])
        self.assertEqual(
            str(context.exception.detail[0]), "Menu item flavors are required."
        )

    def test_if_value(self):
        serializer = MenuItemSerializer()
        self.assertEqual(serializer.validate_menu_item_flavors([1]), [1])


class TestMenuItemSerializerCreate(TestCase):
    def setUp(self):
        self.soda = baker.make(Soda)

        self.flavor1 = baker.make(Flavor)
        self.flavor2 = baker.make(Flavor)
        self.flavor3 = baker.make(Flavor)

        self.limited_time_promo = baker.make(LimitedTimePromotion)

        self.default_data = {
            "name": "Test",
            "soda": self.soda.id,
            "menu_item_flavors": [
                {"flavor": self.flavor1.id, "quantity": 1},
                {"flavor": self.flavor2.id, "quantity": 2},
                {"flavor": self.flavor3.id, "quantity": 3},
            ],
        }

    def test_menu_item_returned(self):
        serializer = MenuItemSerializer(data=self.default_data)
        self.assertTrue(serializer.is_valid())

        menu_item = serializer.save()
        self.assertIsInstance(menu_item, MenuItem)

    def test_menu_item_created(self):
        serializer = MenuItemSerializer(data=self.default_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(MenuItem.objects.count(), 1)

        menu_item = MenuItem.objects.first()
        self.assertEqual(menu_item.name, self.default_data["name"])
        self.assertEqual(menu_item.soda.id, self.default_data["soda"])

    def test_menu_item_flavors_created(self):
        serializer = MenuItemSerializer(data=self.default_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(MenuItem.objects.count(), 1)
        self.assertEqual(MenuItemFlavor.objects.count(), 3)

        menu_item_flavors = MenuItemFlavor.objects.all()
        self.assertEqual(menu_item_flavors[0].flavor.id, self.flavor1.id)
        self.assertEqual(menu_item_flavors[0].quantity, 1)

        self.assertEqual(menu_item_flavors[1].flavor.id, self.flavor2.id)
        self.assertEqual(menu_item_flavors[1].quantity, 2)

        self.assertEqual(menu_item_flavors[2].flavor.id, self.flavor3.id)
        self.assertEqual(menu_item_flavors[2].quantity, 3)

    def test_limited_time_promo_not_created(self):
        serializer = MenuItemSerializer(data=self.default_data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(MenuItem.objects.count(), 1)
        self.assertEqual(MenuItemFlavor.objects.count(), 3)
        self.assertEqual(LimitedTimeMenuItem.objects.count(), 0)

    def test_limited_time_promo_created(self):
        data = self.default_data.copy()
        data["limited_time_promo"] = self.limited_time_promo.id

        serializer = MenuItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(MenuItem.objects.count(), 1)
        self.assertEqual(MenuItemFlavor.objects.count(), 3)
        self.assertEqual(LimitedTimeMenuItem.objects.count(), 1)

        limited_time_menu_item = LimitedTimeMenuItem.objects.first()
        self.assertEqual(
            limited_time_menu_item.menu_item.id, MenuItem.objects.first().id
        )
        self.assertEqual(
            limited_time_menu_item.limited_time_promo.id, self.limited_time_promo.id
        )
