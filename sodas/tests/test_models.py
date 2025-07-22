from django.db import models
from django.test import TestCase
from model_bakery import baker

from sodas.models import Soda


class TestSoda(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(Soda, models.Model))

    def test_str(self):
        soda = baker.make(Soda)
        self.assertEqual(str(soda), soda.name)

    def test_name(self):
        soda = baker.make(Soda)
        field = soda._meta.get_field("name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)
