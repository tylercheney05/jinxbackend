from unittest.mock import patch

from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from cups.models import Cup
from cups.serializers import (
    CupDetailSerializer,
    CupSerializer,
    CupSummarySerializer,
    get_size,
)


class TestGetSize(TestCase):
    def test_size(self):
        cup = baker.make(Cup)
        self.assertEqual(
            get_size(cup),
            {"value": cup.size, "display": cup.get_size_display()},
        )


class TestCupSerializer(TestCase):
    def test_model(self):
        serializer = CupSerializer()
        self.assertEqual(serializer.Meta.model, Cup)

    def test_fields(self):
        serializer = CupSerializer()
        self.assertEqual(
            serializer.Meta.fields, ["id", "size", "price", "conversion_factor"]
        )

    def test_read_only_fields(self):
        serializer = CupSerializer()
        self.assertEqual(serializer.Meta.read_only_fields, ["id"])

    def test_sub_class(self):
        self.assertTrue(issubclass(CupSerializer, serializers.ModelSerializer))


class TestCupSummarySerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(CupSummarySerializer, serializers.ModelSerializer))
        self.assertTrue(issubclass(CupSummarySerializer, ReadOnlyModelSerializer))

    def test_size(self):
        serializer = CupSummarySerializer()
        self.assertIsInstance(
            serializer.fields["size"], serializers.SerializerMethodField
        )

    def test_model(self):
        serializer = CupSummarySerializer()
        self.assertEqual(serializer.Meta.model, Cup)

    def test_fields(self):
        serializer = CupSummarySerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "size"])

    @patch("cups.serializers.get_size")
    def test_get_size(self, mock_get_size):
        cup = baker.make(Cup)
        serializer = CupSummarySerializer(instance=cup)
        serializer.data
        mock_get_size.assert_called_with(cup)


class TestCupDetailSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(CupDetailSerializer, serializers.ModelSerializer))
        self.assertTrue(issubclass(CupDetailSerializer, ReadOnlyModelSerializer))

    def test_size(self):
        serializer = CupDetailSerializer()
        self.assertIsInstance(
            serializer.fields["size"], serializers.SerializerMethodField
        )

    def test_model(self):
        serializer = CupDetailSerializer()
        self.assertEqual(serializer.Meta.model, Cup)

    def test_fields(self):
        serializer = CupDetailSerializer()
        self.assertEqual(
            serializer.Meta.fields, ["id", "size", "price", "conversion_factor"]
        )

    @patch("cups.serializers.get_size")
    def test_get_size(self, mock_get_size):
        cup = baker.make(Cup)
        serializer = CupDetailSerializer(instance=cup)
        serializer.data
        mock_get_size.assert_called_with(cup)
