from django.db import models
from django.test import TestCase
from model_bakery import baker

from menuitems.models import LimitedTimePromotion


class TestLimitedTimePromotion(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(LimitedTimePromotion, models.Model))

    def test_str(self):
        ltp = baker.make(LimitedTimePromotion)
        self.assertEqual(str(ltp), ltp.name)

    def test_name(self):
        field = LimitedTimePromotion._meta.get_field("name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_is_archived(self):
        field = LimitedTimePromotion._meta.get_field("is_archived")
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)
