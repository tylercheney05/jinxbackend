from django.test import TestCase
from model_bakery import baker

from locations.models import Location
from locations.serializers import LocationSerializer


class TestLocationSerializer(TestCase):
    def test_serializer(self):
        location = baker.make(Location)
        serializer = LocationSerializer(location)
        self.assertEqual(
            serializer.data,
            {
                "id": location.id,
                "name": location.name,
            },
        )
