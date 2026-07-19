import math
from decimal import Decimal

from django.db import models

from cups.models import Cup
from menuitems.managers import MenuItemFlavorManager
from menuitems.utils import get_flavors_price
from sodas.constants import (
    WATER_16OZ_PRICE,
    WATER_24OZ_PRICE,
    WATER_32OZ_PRICE,
    WATER_BEVERAGE,
)


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="menu_items"
    )
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def cup_prices(self):
        cup_prices = list()
        for cup in Cup.objects.all().order_by("size"):
            cup_price = cup.price

            ## TODO: REMOVE LATER
            if self.soda.name == WATER_BEVERAGE:
                if cup.size == "16":
                    cup_price = Decimal(WATER_16OZ_PRICE)
                elif cup.size == "24":
                    if self.name == "I Got A Feeling":
                        cup_price = Decimal(2.75)
                    else:
                        cup_price = Decimal(WATER_24OZ_PRICE)
                else:
                    if self.name == "I Got A Feeling":
                        cup_price = Decimal(3)
                    else:
                        cup_price = Decimal(WATER_32OZ_PRICE)

            price = get_flavors_price(self, cup)
            cup_prices.append(
                {
                    "id": cup.id,
                    "size": {
                        "value": cup.size,
                        "display": cup.get_size_display(),
                    },
                    "price": math.ceil((cup_price + price) / Decimal("0.25"))
                    * Decimal("0.25"),
                }
            )
        return cup_prices


class MenuItemFlavor(models.Model):
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="flavors"
    )
    flavor = models.ForeignKey(
        "flavors.Flavor", on_delete=models.CASCADE, related_name="menu_item_flavors"
    )
    quantity = models.PositiveIntegerField()

    objects = MenuItemFlavorManager()

    def __str__(self):
        return f"{self.menu_item.name} {self.flavor.name} {self.quantity}"


class LimitedTimePromotion(models.Model):
    name = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LimitedTimeMenuItem(models.Model):
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="limited_time_promotions"
    )
    limited_time_promo = models.ForeignKey(
        LimitedTimePromotion, on_delete=models.CASCADE, related_name="menu_items"
    )

    def __str__(self):
        return f"{self.menu_item.name} {self.limited_time_promo.name}"


class MenuItemPrice(models.Model):
    """
    This model is used to store the price of a menu item
    not including the price of the cup.
    """

    menu_item = models.OneToOneField(
        MenuItem, on_delete=models.CASCADE, related_name="price"
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Price of the menu_item of a 16 oz drink, not including the price of the cup",
    )

    def __str__(self):
        return f"{self.menu_item.name} {self.price}"
