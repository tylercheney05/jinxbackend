from decimal import Decimal
from unittest.mock import patch

from django.db import models
from django.test import TestCase
from model_bakery import baker

from cups.models import Cup
from menuitems.models import MenuItem
from sodas.constants import WATER_16OZ_PRICE, WATER_32OZ_PRICE


class TestMenuItem(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuItem, models.Model))

    def test_str(self):
        menu_item = baker.make(MenuItem)
        self.assertEqual(str(menu_item), menu_item.name)

    def test_name(self):
        field = MenuItem._meta.get_field("name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_soda(self):
        field = MenuItem._meta.get_field("soda")
        self.assertIsInstance(field, models.ForeignKey)
        self.assertEqual(field.related_model.__name__, "Soda")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "menu_items")

    def test_is_archived(self):
        field = MenuItem._meta.get_field("is_archived")
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)


class TestMenuItemCupPrices(TestCase):
    @patch("menuitems.models.get_flavors_price")
    def test_if_water(self, mock_get_flavors_price):
        mock_get_flavors_price.return_value = 10

        cup1 = baker.make(Cup, size="16", price=Decimal(WATER_16OZ_PRICE))
        cup2 = baker.make(Cup, size="32", price=Decimal(WATER_32OZ_PRICE))
        menu_item = baker.make(MenuItem, soda__name="Water (Flat/Sparkling)")

        self.assertEqual(
            menu_item.cup_prices,
            [
                {
                    "id": cup1.id,
                    "size": {
                        "value": cup1.size,
                        "display": cup1.get_size_display(),
                    },
                    "price": Decimal(WATER_16OZ_PRICE) + 10,
                },
                {
                    "id": cup2.id,
                    "size": {
                        "value": cup2.size,
                        "display": cup2.get_size_display(),
                    },
                    "price": Decimal(WATER_32OZ_PRICE) + 10,
                },
            ],
        )

    @patch("menuitems.models.get_flavors_price")
    def test_if_not_water(self, mock_get_flavors_price):
        mock_get_flavors_price.return_value = 10

        cup1 = baker.make(Cup, size="16", price=Decimal(WATER_16OZ_PRICE))
        cup2 = baker.make(Cup, size="32", price=Decimal(WATER_32OZ_PRICE))
        menu_item = baker.make(MenuItem, soda__name="Cola")

        self.assertEqual(
            menu_item.cup_prices,
            [
                {
                    "id": cup1.id,
                    "size": {
                        "value": cup1.size,
                        "display": cup1.get_size_display(),
                    },
                    "price": cup1.price + 10,
                },
                {
                    "id": cup2.id,
                    "size": {
                        "value": cup2.size,
                        "display": cup2.get_size_display(),
                    },
                    "price": cup2.price + 10,
                },
            ],
        )
