from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F, Sum

from cups.models import Cup


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text="The user who collected the order payment",
        related_name="orders_collected",
    )
    is_paid = models.BooleanField(default=False)
    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text="The user who prepared the items in the order",
        related_name="orders_prepared",
        null=True,
    )
    is_prepared = models.BooleanField(default=False)
    order_name = models.ForeignKey("OrderName", on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    cup = models.ForeignKey("cups.Cup", on_delete=models.CASCADE)
    zero_sugar = models.BooleanField(default=False)
    note = models.TextField(blank=True, default="")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"OrderItem {self.id} - {self.order}"


class CustomOrder(models.Model):
    soda = models.ForeignKey(
        "sodas.Soda", on_delete=models.CASCADE, related_name="custom_orders"
    )

    def __str__(self):
        return f"Custom Order {self.id}"

    @property
    def cup_prices(self):
        cup_prices = list()
        for cup in Cup.objects.all():
            cup_price = cup.price
            price = self.custom_flavors.annotate(
                quantity_price=(F("quantity")) * F("flavor__flavor_group__price")
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


class CustomOrderFlavor(models.Model):
    custom_order = models.ForeignKey(
        "CustomOrder", on_delete=models.CASCADE, related_name="custom_flavors"
    )
    flavor = models.ForeignKey(
        "flavors.Flavor", on_delete=models.CASCADE, related_name="custom_order_flavors"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Custom Order {self.custom_order.id} {self.flavor.name} {self.quantity}"


class OrderName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
