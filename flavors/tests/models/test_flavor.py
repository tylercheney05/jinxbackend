from django.db import models
from django.test import TestCase
from model_bakery import baker

from flavors.models import Flavor


class TestFlavor(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(Flavor, models.Model))

    def test_str(self):
        flavor = baker.make(Flavor)
        self.assertEqual(str(flavor), flavor.name)

    def test_name(self):
        flavor = baker.make(Flavor)
        field = flavor._meta.get_field("name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 200)

    def test_flavor_group(self):
        flavor = baker.make(Flavor)
        field = flavor._meta.get_field("flavor_group")
        self.assertEqual(field.related_model.__name__, "FlavorGroup")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "flavors")

    def test_sugar_free_available(self):
        flavor = baker.make(Flavor)
        field = flavor._meta.get_field("sugar_free_available")
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)
