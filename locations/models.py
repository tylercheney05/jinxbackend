import uuid

from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DeviceToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=100, help_text="e.g. Kitchen iPad 1")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.location.name})"
