from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import FlavorGroup
from flavors.serializers.flavor_group import (
    FlavorGroupSerializer,
    FlavorGroupSerializerReadOnly,
)


class TestFlavorGroupSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(FlavorGroupSerializer, serializers.ModelSerializer))

    def test_model(self):
        serializer = FlavorGroupSerializer()
        self.assertEqual(serializer.Meta.model, FlavorGroup)

    def test_fields(self):
        serializer = FlavorGroupSerializer()
        self.assertEqual(serializer.Meta.fields, ["name", "uom", "price"])


class TestFlavorGroupSerializerReadOnly(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorGroupSerializerReadOnly, serializers.ModelSerializer)
        )
        self.assertTrue(
            issubclass(FlavorGroupSerializerReadOnly, ReadOnlyModelSerializer)
        )

    def test_model(self):
        serializer = FlavorGroupSerializerReadOnly()
        self.assertEqual(serializer.Meta.model, FlavorGroup)

    def test_fields(self):
        serializer = FlavorGroupSerializerReadOnly()
        self.assertEqual(serializer.Meta.fields, ["id", "name", "uom", "price"])

    def test_get_uom(self):
        obj = baker.make(FlavorGroup)
        serializer = FlavorGroupSerializerReadOnly()
        uom = serializer.get_uom(obj)
        self.assertEqual(uom, {"value": obj.uom, "display": obj.get_uom_display()})
