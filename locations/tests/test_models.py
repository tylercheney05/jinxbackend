from django.db import models
from django.test import TestCase
from model_bakery import baker

from locations.models import Location


class TestLocation(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(Location, models.Model))

    def test_str(self):
        location = baker.make(Location)
        self.assertEqual(str(location), location.name)
