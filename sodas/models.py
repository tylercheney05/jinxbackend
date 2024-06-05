from django.db import models

class Soda(models.Model):
    name = models.CharField(max_length=255)
    zero_sugar = models.BooleanField(default=False)

    def __str__(self):
        return self.name