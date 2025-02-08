from django.db import models
from django.test import TestCase
from model_bakery import baker

from cups.models import Cup


class TestCupModel(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(Cup, models.Model))

    def test_str(self):
        cup = baker.make(Cup)
        self.assertEqual(str(cup), cup.size)
