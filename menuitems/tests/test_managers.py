import random
from decimal import Decimal

from django.test import TestCase
from model_bakery import baker

from cups.models import Cup
from flavors.models import Flavor, FlavorGroup
from menuitems.models import MenuItemFlavor


class TestMenuItemFlavorManager(TestCase):
    def test_sum_price(self):
        cup = baker.make(Cup, price=Decimal(round(random.uniform(0, 10), 2)))

        flavor_group1 = baker.make(
            FlavorGroup, price=Decimal(round(random.uniform(0, 10), 2))
        )
        flavor_group2 = baker.make(
            FlavorGroup, price=Decimal(round(random.uniform(0, 10), 2))
        )
        flavor_group3 = baker.make(
            FlavorGroup, price=Decimal(round(random.uniform(0, 10), 2))
        )

        flavor1 = baker.make(Flavor, flavor_group=flavor_group1)
        flavor2 = baker.make(Flavor, flavor_group=flavor_group2)
        flavor3 = baker.make(Flavor, flavor_group=flavor_group3)

        menu_item_flavor1 = baker.make(MenuItemFlavor, flavor=flavor1)
        menu_item_flavor2 = baker.make(MenuItemFlavor, flavor=flavor2)
        menu_item_flavor3 = baker.make(MenuItemFlavor, flavor=flavor3)

        sum_price = MenuItemFlavor.objects.sum_price(cup)

        menu_item_flavor1_price = (
            menu_item_flavor1.quantity * cup.conversion_factor * flavor_group1.price
        )
        menu_item_flavor2_price = (
            menu_item_flavor2.quantity * cup.conversion_factor * flavor_group2.price
        )
        menu_item_flavor3_price = (
            menu_item_flavor3.quantity * cup.conversion_factor * flavor_group3.price
        )

        self.assertEqual(
            round(sum_price["total_sum_product"]),
            round(
                menu_item_flavor1_price
                + menu_item_flavor2_price
                + menu_item_flavor3_price,
            ),
        )
