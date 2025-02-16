from django.db import models
from django.db.models import F, Sum

from cups.models import Cup


class MenuItemFlavorManager(models.Manager):
    def get_queryset(self):
        return MenuItemFlavorQuerySet(self.model, using=self._db)

    def sum_price(self, cup: Cup):
        return self.get_queryset().sum_price(cup)


class MenuItemFlavorQuerySet(models.QuerySet):
    def sum_price(self, cup: Cup):
        return self.annotate(
            quantity_price=(F("quantity") * cup.conversion_factor)
            * F("flavor__flavor_group__price")
        ).aggregate(total_sum_product=Sum("quantity_price"))
