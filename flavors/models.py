from django.db import models


class Flavor(models.Model):
    name = models.CharField(max_length=200)
    flavor_group = models.ForeignKey("FlavorGroup", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FlavorGroup(models.Model):
    uom_choices = [
        ("pump", "Pump"),
        ("tbs", "Tablespoon"),
        ("wedge", "Wedge"),
        ("single", "Single"),
    ]

    name = models.CharField(max_length=200)
    uom = models.CharField(max_length=10, choices=uom_choices)

    def __str__(self):
        return self.name
