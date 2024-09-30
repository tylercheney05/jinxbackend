from django.db import models
from django.db.models import F, Sum

from cups.models import Cup


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="menu_items"
    )

    def __str__(self):
        return self.name

    @property
    def cup_prices(self):
        cup_prices = list()
        for cup in Cup.objects.all():
            cup_price = cup.price
            price = self.flavors.annotate(
                quantity_price=(F("quantity") * cup.conversion_factor)
                * F("flavor__flavor_group__price")
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


class MenuItemFlavor(models.Model):
    menu_item = models.ForeignKey(
        "MenuItem", on_delete=models.CASCADE, related_name="flavors"
    )
    flavor = models.ForeignKey(
        "flavors.Flavor", on_delete=models.CASCADE, related_name="menu_item_flavors"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} {self.flavor.name} {self.quantity}"

    @property
    def cup_quantities(self):
        cup_quantities = dict()
        for cup in Cup.objects.all():
            quantity = self.quantity * cup.conversion_factor
            cup_quantities[cup.id] = quantity
        return cup_quantities


class LimitedTimePromotion(models.Model):
    name = models.CharField(max_length=255)

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
