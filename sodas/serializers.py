from rest_framework import serializers
from sodas.models import Soda

class SodaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "zero_sugar"]
        model = Soda