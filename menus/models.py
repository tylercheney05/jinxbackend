from django.db import models


class Menu(models.Model):
    version = models.PositiveSmallIntegerField()
    date = models.DateField()

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return f"Menu Version {self.version}"
