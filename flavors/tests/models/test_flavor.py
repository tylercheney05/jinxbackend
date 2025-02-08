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
