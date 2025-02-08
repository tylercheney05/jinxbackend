from django.db import models
from django.test import TestCase
from model_bakery import baker

from flavors.models import FlavorGroup


class TestFlavorGroup(TestCase):
    def test_str(self):
        flavor_group = baker.make(FlavorGroup)
        self.assertEqual(str(flavor_group), flavor_group.name)

    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorGroup, models.Model))

    def test_uom_choices(self):
        flavor_group = baker.make(FlavorGroup)
        uom_choices = dict(FlavorGroup.uom_choices)
        self.assertIn(flavor_group.uom, uom_choices.keys())
        self.assertEqual(uom_choices["pump"], "Pump")
        self.assertEqual(uom_choices["tbs"], "Tablespoon")
        self.assertEqual(uom_choices["wedge"], "Wedge")
        self.assertEqual(uom_choices["single"], "Single")
        self.assertEqual(uom_choices["pinch"], "Pinch")
