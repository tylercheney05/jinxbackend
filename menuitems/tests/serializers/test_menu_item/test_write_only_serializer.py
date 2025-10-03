import random
from decimal import Decimal

from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from flavors.models import Flavor
from menuitems.models import LimitedTimePromotion, MenuItem
from menuitems.serializers.limited_time_menu_item import LimitedTimeMenuItemSerializer
from menuitems.serializers.menu_item import MenuItemSerializer
from menuitems.serializers.menu_item_flavor import MenuItemFlavorSerializer
from menuitems.serializers.menu_item_price import MenuItemPriceSerializer
from sodas.models import Soda


class TestMenuItemSerializer(TestCase):
    def test_sub_classes(self):
        assert issubclass(MenuItemSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = MenuItemSerializer()
        self.assertEqual(serializer.Meta.model, MenuItem)

    def test_fields(self):
        serializer = MenuItemSerializer()
        expected_fields = [
            "id",
            "name",
            "soda",
            "is_archived",
            "flavors",
            "limited_time_menu_item",
            "price",
        ]
        self.assertEqual(serializer.Meta.fields, expected_fields)

    def test_extra_kwargs(self):
        serializer = MenuItemSerializer()
        self.assertEqual(
            serializer.Meta.extra_kwargs,
            {
                "is_archived": {"required": False},
            },
        )

    def test_flavors(self):
        serializer = MenuItemSerializer()
        self.assertIsInstance(
            serializer.fields["flavors"].child, MenuItemFlavorSerializer
        )
        self.assertTrue(serializer.fields["flavors"].many)

    def test_limited_time_menu_item(self):
        serializer = MenuItemSerializer()
        self.assertIsInstance(
            serializer.fields["limited_time_menu_item"], LimitedTimeMenuItemSerializer
        )
        self.assertFalse(serializer.fields["limited_time_menu_item"].required)
        self.assertTrue(serializer.fields["limited_time_menu_item"].allow_null)

    def test_price(self):
        serializer = MenuItemSerializer()
        self.assertIsInstance(serializer.fields["price"], MenuItemPriceSerializer)
        self.assertFalse(serializer.fields["price"].required)
        self.assertTrue(serializer.fields["price"].allow_null)

    def test_validate_flavors(self):
        serializer = MenuItemSerializer()
        flavors = []  # Raise error because there are no flavors
        with self.assertRaises(serializers.ValidationError):
            serializer.fields["flavors"].child.run_validation(flavors)


class TestMenuItemSerializerCreateMethod(TestCase):
    def setUp(self):
        self.soda = baker.make(Soda)

        self.flavor1 = baker.make(Flavor)
        self.flavor2 = baker.make(Flavor)

        self.limited_time_promo = baker.make(LimitedTimePromotion)

        self.default_data = {
            "name": "Test Item",
            "soda": self.soda.id,
            "flavors": [
                {"quantity": random.randint(1, 5), "flavor": self.flavor1.id},
                {"quantity": random.randint(1, 5), "flavor": self.flavor2.id},
            ],
        }

    def test_with_just_flavors(self):
        serializer = MenuItemSerializer(data=self.default_data)
        self.assertTrue(serializer.is_valid())
        menu_item = serializer.save()
        self.assertEqual(menu_item.name, "Test Item")
        self.assertEqual(menu_item.soda, self.soda)
        self.assertEqual(menu_item.flavors.count(), 2)
        self.assertIn(
            self.flavor1.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertIn(
            self.flavor2.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )

    def test_with_limited_time_menu_item(self):
        data = self.default_data
        data["limited_time_menu_item"] = {
            "limited_time_promo": self.limited_time_promo.id
        }
        serializer = MenuItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        menu_item = serializer.save()
        self.assertEqual(menu_item.name, "Test Item")
        self.assertEqual(menu_item.soda, self.soda)
        self.assertEqual(menu_item.flavors.count(), 2)
        self.assertIn(
            self.flavor1.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertIn(
            self.flavor2.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertEqual(
            menu_item.limited_time_promotions.first().limited_time_promo,
            self.limited_time_promo,
        )

    def test_with_price(self):
        data = self.default_data
        price = Decimal(f"{random.uniform(1.00, 5.00):.2f}")
        data["price"] = {"price": price}
        serializer = MenuItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        menu_item = serializer.save()
        self.assertEqual(menu_item.name, "Test Item")
        self.assertEqual(menu_item.soda, self.soda)
        self.assertEqual(menu_item.flavors.count(), 2)
        self.assertIn(
            self.flavor1.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertIn(
            self.flavor2.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertEqual(menu_item.price.price, price)

    def test_with_limited_time_menu_item_and_price(self):
        data = self.default_data
        price = Decimal(f"{random.uniform(1.00, 5.00):.2f}")
        data["price"] = {"price": price}
        data["limited_time_menu_item"] = {
            "limited_time_promo": self.limited_time_promo.id
        }
        serializer = MenuItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        menu_item = serializer.save()
        self.assertEqual(menu_item.name, "Test Item")
        self.assertEqual(menu_item.soda, self.soda)
        self.assertEqual(menu_item.flavors.count(), 2)
        self.assertIn(
            self.flavor1.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertIn(
            self.flavor2.id,
            list(menu_item.flavors.all().values_list("flavor", flat=True)),
        )
        self.assertEqual(menu_item.price.price, price)
        self.assertEqual(
            menu_item.limited_time_promotions.first().limited_time_promo,
            self.limited_time_promo,
        )
