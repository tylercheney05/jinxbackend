from django.test import TestCase
from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer


class TestReadOnlyModelSerializer(TestCase):
    def test_create(self):
        serializer = ReadOnlyModelSerializer()
        with self.assertRaises(serializers.ValidationError) as error:
            serializer.create({})
        self.assertEqual(
            str(error.exception.detail[0]),
            "Read-only serializer does not have write access",
        )

    def test_update(self):
        serializer = ReadOnlyModelSerializer()
        with self.assertRaises(serializers.ValidationError) as error:
            serializer.update({}, {})
        self.assertEqual(
            str(error.exception.detail[0]),
            "Read-only serializer does not have write access",
        )
