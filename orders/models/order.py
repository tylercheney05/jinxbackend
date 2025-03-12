from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from orders.constants import ORDER_ITEMS_ATTRS
from orders.managers import OrderManager


class Order(models.Model):
    date = models.DateTimeField()
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
    is_complete = models.BooleanField(default=False)
    order_name = models.ForeignKey("OrderName", on_delete=models.PROTECT, null=True)
    is_in_progress = models.BooleanField(default=False)

    objects = OrderManager()

    def __str__(self):
        return f"Order {self.id} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        super().save(*args, **kwargs)

    @property
    def pending_price(self):
        # Price before the customer has paid
        # Does not represent the price of the order
        price = 0
        for item in self.items.all():
            for attr in ORDER_ITEMS_ATTRS:
                if hasattr(item, attr):
                    price += getattr(item, attr).price
                    break
        decimal_price = Decimal(price)
        return decimal_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class OrderPaidAmount(models.Model):
    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="paid_amount"
    )
    paid_amount = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"OrderPaidAmount {self.id}"


class OrderName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class OrderDiscount(models.Model):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE)
    discount = models.ForeignKey("orders.Discount", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.discount.name}"
