from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import FlavorGroup
from flavors.serializers import (
    FlavorGroupDetailSerializer,
    FlavorGroupSerializer,
    FlavorGroupSummarySerializer,
)


class TestFlavorGroupSerializer(TestCase):
    def test_serializer(self):
        flavor_group = baker.make(FlavorGroup)
        serializer = FlavorGroupSerializer(flavor_group)
        self.assertEqual(
            serializer.data,
            {
                "name": flavor_group.name,
                "uom": flavor_group.uom,
                "price": str(flavor_group.price),
            },
        )

    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorGroupSerializer, serializers.ModelSerializer))


class TestFlavorGroupSummarySerializer(TestCase):
    def test_serializer(self):
        flavor_group = baker.make(FlavorGroup)
        serializer = FlavorGroupSummarySerializer(flavor_group)
        self.assertEqual(
            serializer.data,
            {
                "id": flavor_group.id,
                "name": flavor_group.name,
                "uom": {
                    "value": flavor_group.uom,
                    "display": flavor_group.get_uom_display(),
                },
                "price": str(flavor_group.price),
            },
        )

    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorGroupSummarySerializer, ReadOnlyModelSerializer)
        )


class TestFlavorGroupDetailSerializer(TestCase):
    def test_serializer(self):
        flavor_group = baker.make(FlavorGroup)
        serializer = FlavorGroupDetailSerializer(flavor_group)
        self.assertEqual(
            serializer.data,
            {
                "id": flavor_group.id,
                "uom": {
                    "value": flavor_group.uom,
                    "display": flavor_group.get_uom_display(),
                },
            },
        )

    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorGroupDetailSerializer, ReadOnlyModelSerializer)
        )
