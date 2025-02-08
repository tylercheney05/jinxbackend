from django.test import TestCase
from model_bakery import baker

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
