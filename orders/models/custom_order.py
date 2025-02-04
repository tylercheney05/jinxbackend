from django.apps import apps
from django.db import models
from django.db.models import F, Sum


class CustomOrder(models.Model):
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="custom_orders"
    )

    def __str__(self):
        return f"Custom Order {self.id}"

    @property
    def cup_prices(self):
        cup_prices = list()
        cup_model = apps.get_model("cups", "Cup")
        for cup in cup_model.objects.all():
            cup_price = cup.price
            price = self.custom_order_custom_order_flavors.annotate(
                quantity_price=(
                    F("custom_order_flavor__quantity")
                    * F("custom_order_flavor__flavor__flavor_group__price")
                )
            ).aggregate(total_sum_product=Sum("quantity_price"))
            total_sum_product = price.get("total_sum_product", 0)
            flavors_price = total_sum_product if total_sum_product else 0
            cup_prices.append(
                {
                    "id": cup.id,
                    "size": cup.size,
                    "size__display": cup.get_size_display(),
                    "price": cup_price + flavors_price,
                }
            )
        return cup_prices


class MenuItemCustomOrder(models.Model):
    """The same thing as CustomOrder except this associates it to a menu item"""

    menu_item = models.ForeignKey(
        "menuitems.MenuItem", on_delete=models.CASCADE, related_name="custom_orders"
    )
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="menu_item_custom_orders"
    )

    def __str__(self):
        return f"MenuItemCustomOrder {self.id}"

    @property
    def cup_prices(self):
        cup_prices = list()
        cup_model = apps.get_model("cups", "Cup")
        for cup in cup_model.objects.all():
            cup_price = cup.price
            price = self.menu_item_custom_order_custom_order_flavors.annotate(
                quantity_price=(
                    F("custom_order_flavor__quantity")
                    * F("custom_order_flavor__flavor__flavor_group__price")
                )
            ).aggregate(total_sum_product=Sum("quantity_price"))
            cup_prices.append(
                {
                    "id": cup.id,
                    "size": cup.size,
                    "size__display": cup.get_size_display(),
                    "price": cup_price + price.get("total_sum_product", 0),
                }
            )
        return cup_prices
