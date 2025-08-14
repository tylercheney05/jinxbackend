from django.test import TestCase
from rest_framework import serializers

from locations.models import Location
from locations.serializers import LocationSerializer


class TestLocationSerializer(TestCase):
    def test_sub_class(self):
        assert issubclass(LocationSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = LocationSerializer()
        self.assertEqual(serializer.Meta.model, Location)

    def test_fields(self):
        serializer = LocationSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "name"])
