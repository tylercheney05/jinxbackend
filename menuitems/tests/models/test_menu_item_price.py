from django.db import models
from django.test import TestCase
from model_bakery import baker

from menuitems.models import MenuItemPrice


class MenuItemPriceTest(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuItemPrice, models.Model))

    def test_menu_item(self):
        model = MenuItemPrice()
        field = model._meta.get_field("menu_item")
        self.assertEqual(field.related_model.__name__, "MenuItem")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "price")

    def test_price(self):
        model = MenuItemPrice()
        field = model._meta.get_field("price")
        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 5)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(
            field.help_text,
            "Price of the menu_item of a 16 oz drink, not including the price of the cup",
        )

    def test_str(self):
        menu_item_price = baker.make(MenuItemPrice)
        self.assertEqual(
            str(menu_item_price),
            f"{menu_item_price.menu_item.name} {menu_item_price.price}",
        )
