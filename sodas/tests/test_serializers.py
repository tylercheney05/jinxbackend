from django.test import TestCase
from rest_framework import serializers

from sodas.models import Soda
from sodas.serializers import SodaSerializer


class TestSodaSerializer(TestCase):
    def test_sub_class(self):
        assert issubclass(SodaSerializer, serializers.ModelSerializer)

    def test_model(self):
        serializer = SodaSerializer()
        self.assertEqual(serializer.Meta.model, Soda)

    def test_fields(self):
        serializer = SodaSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "name"])
