from django.db import models
from django.test import TestCase
from model_bakery import baker

from menus.models import Menu


class TestMenu(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(Menu, models.Model))

    def test_str(self):
        menu = baker.make(Menu)
        self.assertEqual(str(menu), f"Menu Version {menu.version}")

    def test_version(self):
        menu = baker.make(Menu)
        field = menu._meta.get_field("version")
        self.assertIsInstance(field, models.PositiveSmallIntegerField)
        self.assertTrue(field.unique)

    def test_date(self):
        menu = baker.make(Menu)
        field = menu._meta.get_field("date")
        self.assertIsInstance(field, models.DateField)
        self.assertTrue(field.unique)

    def test_verbose_name(self):
        self.assertEqual(Menu._meta.verbose_name, "Menu")
        self.assertEqual(Menu._meta.verbose_name_plural, "Menus")
