from django.test import TestCase
from rest_framework import mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUser
from flavors.models import FlavorGroup
from flavors.serializers import FlavorGroupSerializer, FlavorGroupSummarySerializer
from flavors.views import FlavorGroupViewSet


class TestFlavorGroupViewSet(TestCase):
    def test_sub_classes(self):
        view = FlavorGroupViewSet()
        self.assertTrue(issubclass(view.__class__, viewsets.GenericViewSet))
        self.assertTrue(issubclass(view.__class__, mixins.CreateModelMixin))
        self.assertTrue(issubclass(view.__class__, mixins.ListModelMixin))
        self.assertTrue(issubclass(view.__class__, AutocompleteViewSetMixin))

    def test_http_method_names(self):
        view = FlavorGroupViewSet()
        self.assertEqual(view.http_method_names, ["post", "get"])

    def test_model(self):
        view = FlavorGroupViewSet()
        self.assertEqual(view.model, FlavorGroup)

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
    def test_list(self):
        view = FlavorGroupViewSet()
        view.action = "list"
        self.assertEqual(view.get_serializer_class(), FlavorGroupSummarySerializer)

    def test_default(self):
        view = FlavorGroupViewSet()
        view.action = "default"
        self.assertEqual(view.get_serializer_class(), FlavorGroupSerializer)
