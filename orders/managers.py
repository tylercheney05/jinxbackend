from django.db import models
from django.db.models import BooleanField, Case, F, IntegerField, Value, When


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def pending_orders(self, location_id):
        return self.get_queryset().pending_orders(location_id=location_id)


class OrderQuerySet(models.QuerySet):
    def pending_orders(self, location_id):
        return (
            self.filter(
                location_id=location_id,
                is_paid=True,
            )
            .annotate(
                is_complete_order=Case(
                    When(is_complete=True, then=Value(1)),
                    When(is_complete=False, then=Value(0)),
                    output_field=BooleanField(),
                ),
                order_id=Case(
                    When(is_complete=True, then=-F("id")),
                    When(is_complete=False, then=F("id")),
                    output_field=IntegerField(),
                ),
            )
            .order_by("is_complete_order", "order_id")[:10]
        )
