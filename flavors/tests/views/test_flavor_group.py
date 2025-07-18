from django.test import TestCase
from rest_framework import mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUser
from flavors.models import FlavorGroup
from flavors.serializers.flavor_group import (
    FlavorGroupSerializer,
    FlavorGroupSerializerReadOnly,
)
from flavors.views import FlavorGroupViewSet


class TestFlavorGroupViewSet(TestCase):
    def test_sub_classes(self):
        view = FlavorGroupViewSet()
        self.assertTrue(issubclass(view.__class__, viewsets.GenericViewSet))
        self.assertTrue(issubclass(view.__class__, mixins.CreateModelMixin))
        self.assertTrue(issubclass(view.__class__, mixins.ListModelMixin))
        self.assertTrue(issubclass(view.__class__, AutocompleteViewSetMixin))
        self.assertTrue(issubclass(view.__class__, mixins.UpdateModelMixin))

    def test_http_method_names(self):
        view = FlavorGroupViewSet()
        self.assertEqual(view.http_method_names, ["post", "get", "put"])

    def test_queryset(self):
        view = FlavorGroupViewSet()
        self.assertQuerySetEqual(
            view.queryset, FlavorGroup.objects.all(), transform=lambda x: x
        )

    def test_permission_classes(self):
        view = FlavorGroupViewSet()
        self.assertEqual(view.permission_classes, [IsSystemAdminUser])

    def test_autocomplete_fields(self):
        view = FlavorGroupViewSet()
        self.assertEqual(view.autocomplete_fields, ["id", "name"])


class TestGetSerializerClass(TestCase):
    def test_create(self):
        view = FlavorGroupViewSet()
        view.action = "create"
        self.assertEqual(view.get_serializer_class(), FlavorGroupSerializer)

    def test_update(self):
        view = FlavorGroupViewSet()
        view.action = "update"
        self.assertEqual(view.get_serializer_class(), FlavorGroupSerializer)

    def test_default(self):
        view = FlavorGroupViewSet()
        view.action = "default"
        self.assertEqual(view.get_serializer_class(), FlavorGroupSerializerReadOnly)
