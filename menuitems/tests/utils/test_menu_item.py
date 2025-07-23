from unittest.mock import patch

from django.test import TestCase
from model_bakery import baker

from cups.models import Cup
from menuitems.models import MenuItem, MenuItemPrice
from menuitems.utils import get_flavors_price


class TestGetFlavorsPrice(TestCase):
    @patch("menuitems.models.MenuItemFlavorManager.sum_price")
    def test_if_no_manual_price(self, mock_sum_price):
        mock_sum_price.return_value = {"total_sum_product": 10}

        cup = baker.make(Cup)
        menu_item = baker.make(MenuItem)
        value = get_flavors_price(menu_item, cup)

        self.assertEqual(
            value,
            10,
        )

    def test_if_manual_price(self):
        cup = baker.make(Cup)
        menu_item = baker.make(MenuItem)
        menu_item_price = baker.make(MenuItemPrice, menu_item=menu_item)
        value = get_flavors_price(menu_item, cup)

        self.assertEqual(
            value,
            menu_item_price.price * cup.conversion_factor,
        )
