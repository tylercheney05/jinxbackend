from rest_framework import serializers
from flavors.models import Flavor


class FlavorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Flavor
    fields = ["name"]
