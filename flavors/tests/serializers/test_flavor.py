from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import Flavor
from flavors.serializers import (
    FlavorDetailSerializer,
    FlavorSerializer,
    FlavorSummarySerializer,
)


class TestFlavorSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorSerializer, serializers.ModelSerializer))

    def test_serializer(self):
        flavor = baker.make(Flavor)
        serializer = FlavorSerializer(flavor)
        self.assertEqual(
            serializer.data,
            {
                "id": flavor.id,
                "name": flavor.name,
                "flavor_group": flavor.flavor_group.id,
                "sugar_free_available": flavor.sugar_free_available,
            },
        )


class TestFlavorDetailSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorDetailSerializer, serializers.ModelSerializer))
        self.assertTrue(issubclass(FlavorDetailSerializer, ReadOnlyModelSerializer))

    def test_serializer(self):
        flavor = baker.make(Flavor)
        serializer = FlavorDetailSerializer(flavor)
        self.assertEqual(
            serializer.data,
            {
                "id": flavor.id,
                "name": flavor.name,
                "flavor_group": {
                    "id": flavor.flavor_group.id,
                    "uom": {
                        "value": flavor.flavor_group.uom,
                        "display": flavor.flavor_group.get_uom_display(),
                    },
                },
                "sugar_free_available": flavor.sugar_free_available,
            },
        )


class TestFlavorSummarySerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorSummarySerializer, serializers.ModelSerializer)
        )
        self.assertTrue(issubclass(FlavorSummarySerializer, ReadOnlyModelSerializer))

    def test_serializer(self):
        flavor = baker.make(Flavor)
        serializer = FlavorSummarySerializer(flavor)
        self.assertEqual(
            serializer.data,
            {
                "id": flavor.id,
                "name": flavor.name,
                "flavor_group": {
                    "id": flavor.flavor_group.id,
                    "name": flavor.flavor_group.name,
                    "uom": {
                        "value": flavor.flavor_group.uom,
                        "display": flavor.flavor_group.get_uom_display(),
                    },
                    "price": str(flavor.flavor_group.price),
                },
            },
        )
