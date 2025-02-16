from django.db import models
from django.test import TestCase
from model_bakery import baker

from cups.models import Cup


class TestCupModel(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(Cup, models.Model))

    def test_size_choices(self):
        model = Cup()
        self.assertEqual(
            model.size_choices,
            [
                ("16", "16 oz"),
                ("32", "32 oz"),
            ],
        )

    def test_size(self):
        model = Cup()
        field = model._meta.get_field("size")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 10)
        self.assertEqual(field.choices, model.size_choices)

    def test_price(self):
        model = Cup()
        field = model._meta.get_field("price")
        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 5)
        self.assertEqual(field.decimal_places, 2)

    def test_conversion_factor(self):
        model = Cup()
        field = model._meta.get_field("conversion_factor")
        self.assertIsInstance(field, models.DecimalField)
        self.assertEqual(field.max_digits, 5)
        self.assertEqual(field.decimal_places, 2)

    def test_str(self):
        cup = baker.make(Cup)
        self.assertEqual(str(cup), cup.size)
