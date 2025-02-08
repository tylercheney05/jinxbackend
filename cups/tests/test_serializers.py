from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from cups.models import Cup
from cups.serializers import CupDetailSerializer, CupSerializer, CupSummarySerializer


class TestCupSerializer(TestCase):
    def test_serializer(self):
        cup = baker.make(Cup)
        serializer = CupSerializer(cup)
        self.assertEqual(
            serializer.data,
            {
                "id": cup.id,
                "size": cup.size,
                "price": str(cup.price),
                "conversion_factor": str(cup.conversion_factor),
            },
        )

    def test_sub_class(self):
        self.assertTrue(issubclass(CupSerializer, serializers.ModelSerializer))


class TestCupSummarySerializer(TestCase):
    def test_serializer(self):
        cup = baker.make(Cup)
        serializer = CupSummarySerializer(cup)
        self.assertEqual(
            serializer.data,
            {
                "id": cup.id,
                "size": {"value": cup.size, "display": cup.get_size_display()},
            },
        )

    def test_sub_class(self):
        self.assertTrue(issubclass(CupSummarySerializer, serializers.ModelSerializer))
        self.assertTrue(issubclass(CupSummarySerializer, ReadOnlyModelSerializer))


class TestCupDetailSerializer(TestCase):
    def test_serializer(self):
        cup = baker.make(Cup)
        serializer = CupDetailSerializer(cup)
        self.assertEqual(
            serializer.data,
            {
                "id": cup.id,
                "size": {"value": cup.size, "display": cup.get_size_display()},
                "price": str(cup.price),
                "conversion_factor": str(cup.conversion_factor),
            },
        )

    def test_sub_class(self):
        self.assertTrue(issubclass(CupDetailSerializer, serializers.ModelSerializer))
        self.assertTrue(issubclass(CupDetailSerializer, ReadOnlyModelSerializer))
