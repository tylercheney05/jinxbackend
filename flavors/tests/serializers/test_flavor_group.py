from unittest.mock import patch

from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.models import FlavorGroup
from flavors.serializers import (
    FlavorGroupDetailSerializer,
    FlavorGroupSerializer,
    FlavorGroupSummarySerializer,
    get_uom,
)


class TestGetUom(TestCase):
    def test_get_uom(self):
        obj = baker.make(FlavorGroup)
        self.assertEqual(
            get_uom(obj), {"value": obj.uom, "display": obj.get_uom_display()}
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


class TestFlavorGroupSummarySerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorGroupSummarySerializer, serializers.ModelSerializer)
        )
        self.assertTrue(
            issubclass(FlavorGroupSummarySerializer, ReadOnlyModelSerializer)
        )

    def test_model(self):
        serializer = FlavorGroupSummarySerializer()
        self.assertEqual(serializer.Meta.model, FlavorGroup)

    def test_fields(self):
        serializer = FlavorGroupSummarySerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "name", "uom", "price"])

    @patch("flavors.serializers.flavor_group.get_uom")
    def test_get_uom(self, mock_get_uom):
        obj = baker.make(FlavorGroup)
        serializer = FlavorGroupSummarySerializer()
        serializer.get_uom(obj)
        mock_get_uom.assert_called_with(obj)


class TestFlavorGroupDetailSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(
            issubclass(FlavorGroupDetailSerializer, serializers.ModelSerializer)
        )
        self.assertTrue(
            issubclass(FlavorGroupDetailSerializer, ReadOnlyModelSerializer)
        )

    def test_model(self):
        serializer = FlavorGroupDetailSerializer()
        self.assertEqual(serializer.Meta.model, FlavorGroup)

    def test_fields(self):
        serializer = FlavorGroupDetailSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "uom"])

    @patch("flavors.serializers.flavor_group.get_uom")
    def test_get_uom(self, mock_get_uom):
        obj = baker.make(FlavorGroup)
        serializer = FlavorGroupDetailSerializer()
        serializer.get_uom(obj)
        mock_get_uom.assert_called_with(obj)
