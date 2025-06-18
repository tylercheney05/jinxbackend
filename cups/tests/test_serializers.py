from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from cups.models import Cup
from cups.serializers import CupSerializer, CupSerializerReadOnly


class TestCupSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(CupSerializer, serializers.ModelSerializer))

    def test_model(self):
        serializer = CupSerializer()
        self.assertEqual(serializer.Meta.model, Cup)

    def test_fields(self):
        serializer = CupSerializer()
        self.assertEqual(
            serializer.Meta.fields, ["id", "size", "price", "conversion_factor"]
        )


class TestCupSerializerReadOnly(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(CupSerializerReadOnly, serializers.ModelSerializer))
        self.assertTrue(issubclass(CupSerializerReadOnly, ReadOnlyModelSerializer))

    def test_size(self):
        serializer = CupSerializerReadOnly()
        self.assertIsInstance(
            serializer.fields["size"], serializers.SerializerMethodField
        )

    def test_model(self):
        serializer = CupSerializerReadOnly()
        self.assertEqual(serializer.Meta.model, Cup)

    def test_fields(self):
        serializer = CupSerializerReadOnly()
        self.assertEqual(
            serializer.Meta.fields, ["id", "size", "price", "conversion_factor"]
        )

    def test_get_size(self):
        cup = baker.make(Cup)
        size = CupSerializerReadOnly().get_size(cup)
        self.assertEqual(size, {"value": cup.size, "display": cup.get_size_display()})
