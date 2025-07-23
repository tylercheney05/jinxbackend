from django.db import models
from django.test import TestCase
from model_bakery import baker

from menuitems.managers import MenuItemFlavorManager
from menuitems.models import MenuItemFlavor


class TestMenuItemFlavor(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuItemFlavor, models.Model))

    def test_str(self):
        menu_item_flavor = baker.make(MenuItemFlavor)

        self.assertEqual(
            str(menu_item_flavor),
            f"{menu_item_flavor.menu_item.name} {menu_item_flavor.flavor.name} {menu_item_flavor.quantity}",
        )

    def test_menu_item(self):
        model = MenuItemFlavor()
        field = model._meta.get_field("menu_item")
        self.assertEqual(field.related_model.__name__, "MenuItem")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "flavors")

    def test_flavor(self):
        model = MenuItemFlavor()
        field = model._meta.get_field("flavor")
        self.assertEqual(field.related_model.__name__, "Flavor")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "menu_item_flavors")

    def test_quantity(self):
        model = MenuItemFlavor()
        field = model._meta.get_field("quantity")
        self.assertIsInstance(field, models.PositiveIntegerField)

    def test_objects(self):
        self.assertIsInstance(MenuItemFlavor.objects, MenuItemFlavorManager)
