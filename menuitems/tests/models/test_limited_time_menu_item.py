from django.db import models
from django.test import TestCase
from model_bakery import baker

from menuitems.models import LimitedTimeMenuItem


class LimitedTimePromotionTest(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(LimitedTimeMenuItem, models.Model))

    def test_menu_item(self):
        model = LimitedTimeMenuItem()
        field = model._meta.get_field("menu_item")
        self.assertEqual(field.related_model.__name__, "MenuItem")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "limited_time_promotions")

    def test_limited_time_promo(self):
        model = LimitedTimeMenuItem()
        field = model._meta.get_field("limited_time_promo")
        self.assertEqual(field.related_model.__name__, "LimitedTimePromotion")
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(field.remote_field.related_name, "menu_items")

    def test_str(self):
        limited_time_menu_item = baker.make(LimitedTimeMenuItem)
        self.assertEqual(
            str(limited_time_menu_item),
            f"{limited_time_menu_item.menu_item.name} {limited_time_menu_item.limited_time_promo.name}",
        )
