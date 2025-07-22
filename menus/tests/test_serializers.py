from django.test import TestCase
from rest_framework import serializers

from menus.models import Menu
from menus.serializers import MenuSerializer


class TestMenuSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(MenuSerializer, serializers.ModelSerializer))

    def test_model(self):
        serializer = MenuSerializer()
        self.assertEqual(serializer.Meta.model, Menu)

    def test_fields(self):
        serializer = MenuSerializer()
        self.assertEqual(serializer.Meta.fields, ["id", "version", "date"])
