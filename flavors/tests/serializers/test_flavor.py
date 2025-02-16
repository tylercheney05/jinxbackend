from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import Flavor
from flavors.serializers import (
    FlavorDetailSerializer,
    FlavorGroupDetailSerializer,
    FlavorGroupSummarySerializer,
    FlavorSerializer,
    FlavorSummarySerializer,
)


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
            ["id", "name", "flavor_group", "sugar_free_available"],
        )

    def test_read_only_fields(self):
        serializer = FlavorSerializer()
        self.assertEqual(serializer.Meta.read_only_fields, ["id"])


class TestFlavorDetailSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorDetailSerializer, serializers.ModelSerializer))
        self.assertTrue(issubclass(FlavorDetailSerializer, ReadOnlyModelSerializer))

    def test_flavor_group(self):
        serializer = FlavorDetailSerializer()
        self.assertIsInstance(
            serializer.fields["flavor_group"], FlavorGroupDetailSerializer
        )

    def test_model(self):
        serializer = FlavorDetailSerializer()
        self.assertEqual(serializer.Meta.model, Flavor)

    def test_fields(self):
        serializer = FlavorDetailSerializer()
        self.assertEqual(
            serializer.Meta.fields,
            ["id", "name", "flavor_group", "sugar_free_available"],
        )


class TestFlavorSummarySerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorSummarySerializer, serializers.ModelSerializer)
        )
        self.assertTrue(issubclass(FlavorSummarySerializer, ReadOnlyModelSerializer))

    def test_flavor_group(self):
        serializer = FlavorSummarySerializer()
        self.assertIsInstance(
            serializer.fields["flavor_group"], FlavorGroupSummarySerializer
        )

    def test_model(self):
        serializer = FlavorSummarySerializer()
        self.assertEqual(serializer.Meta.model, Flavor)

    def test_fields(self):
        serializer = FlavorSummarySerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "name", "flavor_group"])
