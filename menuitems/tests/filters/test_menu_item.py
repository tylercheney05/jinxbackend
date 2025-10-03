import django_filters
from django.test import TestCase

from menuitems.filters import MenuItemFilter
from menuitems.models import MenuItem


class TestMenuItemFilter(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuItemFilter, django_filters.FilterSet))

    def test_limited_time_promotions__isnull(self):
        filter = MenuItemFilter()
        self.assertIsInstance(
            filter.filters["limited_time_promotions__isnull"],
            django_filters.BooleanFilter,
        )
        self.assertEqual(
            filter.filters["limited_time_promotions__isnull"].field_name,
            "limited_time_promotions",
        )
        self.assertEqual(
            filter.filters["limited_time_promotions__isnull"].lookup_expr,
            "isnull",
        )

    def test_model(self):
        filter = MenuItemFilter()
        self.assertEqual(filter.Meta.model, MenuItem)

    def test_fields(self):
        filter = MenuItemFilter()
        self.assertEqual(
            filter.Meta.fields,
            [
                "soda",
                "is_archived",
                "limited_time_promotions__limited_time_promo",
                "limited_time_promotions__isnull",
                "limited_time_promotions__limited_time_promo__is_archived",
            ],
        )
