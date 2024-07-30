from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField(default=0)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    is_paid = models.BooleanField(default=False)
    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return f"Order {self.id} - {self.date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    cup = models.ForeignKey("cups.Cup", on_delete=models.CASCADE)
    zero_sugar = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"OrderItem {self.id} - {self.order}"
