from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    is_event = models.BooleanField(default=False)

    def __str__(self):
        return self.name
