from unittest.mock import patch

from django.db import models
from django.test import TestCase
from model_bakery import baker

from cups.models import Cup
from menuitems.models import MenuItem, MenuItemPrice


class TestMenuItem(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuItem, models.Model))

    def test_name(self):
        model = MenuItem()
        field = model._meta.get_field("name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_soda(self):
        model = MenuItem()
        field = model._meta.get_field("soda")
        self.assertEqual(field.related_model.__name__, "Soda")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "menu_items")

    def test_str(self):
        menu_item = baker.make(MenuItem)
        self.assertEqual(str(menu_item), menu_item.name)


class TestCupPrices(TestCase):
    @patch("menuitems.models.MenuItemFlavorManager.sum_price")
    def test_if_no_manual_price(self, mock_sum_price):
        mock_sum_price.return_value = {"total_sum_product": 10}

        cup1 = baker.make(Cup)
        cup2 = baker.make(Cup)

        menu_item = baker.make(MenuItem)

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

    def test_if_manual_price(self):
        cup1 = baker.make(Cup)
        cup2 = baker.make(Cup)

        menu_item = baker.make(MenuItem)
        menu_item_price = baker.make(MenuItemPrice, menu_item=menu_item)

        self.assertEqual(
            menu_item.cup_prices,
            [
                {
                    "id": cup1.id,
                    "size": {
                        "value": cup1.size,
                        "display": cup1.get_size_display(),
                    },
                    "price": cup1.price
                    + menu_item_price.price * cup1.conversion_factor,
                },
                {
                    "id": cup2.id,
                    "size": {
                        "value": cup2.size,
                        "display": cup2.get_size_display(),
                    },
                    "price": cup2.price
                    + menu_item_price.price * cup2.conversion_factor,
                },
            ],
        )
