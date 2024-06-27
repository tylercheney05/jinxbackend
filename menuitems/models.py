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
        cup_prices = dict()
        for cup in Cup.objects.all():
            cup_price = cup.price
            price = self.flavors.annotate(
                quantity_price=(F("quantity") * cup.conversion_factor)
                * F("flavor__flavor_group__price")
            ).aggregate(total_sum_product=Sum("quantity_price"))
            cup_prices[cup.get_size_display()] = cup_price + price.get(
                "total_sum_product", 0
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
