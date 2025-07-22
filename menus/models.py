from django.db import models


class Menu(models.Model):
    version = models.PositiveSmallIntegerField(unique=True)
    date = models.DateField(unique=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return f"Menu Version {self.version}"
