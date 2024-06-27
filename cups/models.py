from django.db import models


class Cup(models.Model):
    size_choices = [
        ("16", "16 oz"),
        ("32", "32 oz"),
    ]

    size = models.CharField(max_length=10, choices=size_choices)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    conversion_factor = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.size
