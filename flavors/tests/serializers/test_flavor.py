from django.test import TestCase
from rest_framework import serializers

from flavors.models import Flavor
from flavors.serializers.flavor import FlavorSerializer, FlavorSerializerReadOnly
from flavors.serializers.flavor_group import FlavorGroupSerializerReadOnly


class TestFlavorSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorSerializer, serializers.ModelSerializer))

    def test_model(self):
        serializer = FlavorSerializer()
        self.assertEqual(serializer.Meta.model, Flavor)

    def test_fields(self):
        serializer = FlavorSerializer()
        self.assertEqual(
            serializer.Meta.fields,
            ["name", "flavor_group", "sugar_free_available"],
        )


class TestFlavorSerializerReadOnly(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorSerializerReadOnly, serializers.ModelSerializer)
        )

    def test_flavor_group(self):
        serializer = FlavorSerializerReadOnly()
        self.assertIsInstance(
            serializer.fields["flavor_group"], FlavorGroupSerializerReadOnly
        )

    def test_model(self):
        serializer = FlavorSerializerReadOnly()
        self.assertEqual(serializer.Meta.model, Flavor)

    def test_fields(self):
        serializer = FlavorSerializerReadOnly()
        self.assertEqual(
            serializer.Meta.fields,
            ["id", "name", "flavor_group", "sugar_free_available"],
        )
