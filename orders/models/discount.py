from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class DiscountPercentOff(models.Model):
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)
    percent_off = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    def __str__(self):
        return f"{self.discount.name} - {self.percent_off * 100}% off"


class DiscountPrice(models.Model):
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.discount.name} - ${self.price}"


class DiscountCupSize(models.Model):
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE)
    cup = models.ForeignKey("cups.Cup", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.discount.name} - {self.cup.size}"
