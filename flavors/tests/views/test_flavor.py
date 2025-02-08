from django.test import TestCase
from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUser
from flavors.models import Flavor
from flavors.serializers import (
    FlavorDetailSerializer,
    FlavorSerializer,
    FlavorSummarySerializer,
)
from flavors.views import FlavorViewSet


class TestFlavorViewSet(TestCase):
    def test_sub_classes(self):
        view = FlavorViewSet()
        self.assertTrue(issubclass(view.__class__, viewsets.GenericViewSet))
        self.assertTrue(issubclass(view.__class__, mixins.CreateModelMixin))
        self.assertTrue(issubclass(view.__class__, mixins.ListModelMixin))
        self.assertTrue(issubclass(view.__class__, AutocompleteViewSetMixin))
        self.assertTrue(issubclass(view.__class__, mixins.RetrieveModelMixin))

    def test_http_method_names(self):
        view = FlavorViewSet()
        self.assertEqual(view.http_method_names, ["post", "get"])

    def test_model(self):
        view = FlavorViewSet()
        self.assertEqual(view.model, Flavor)

    def test_queryset(self):
        view = FlavorViewSet()
        self.assertQuerySetEqual(
            view.queryset, Flavor.objects.all(), transform=lambda x: x
        )

    def test_permission_classes(self):
        view = FlavorViewSet()
        self.assertEqual(view.permission_classes, [IsSystemAdminUser])

    def test_autocomplete_fields(self):
        view = FlavorViewSet()
        self.assertEqual(view.autocomplete_fields, ["id", "name"])

    def test_filter_backends(self):
        view = FlavorViewSet()
        self.assertEqual(view.filter_backends, [filters.OrderingFilter])

    def test_ordering_fields(self):
        view = FlavorViewSet()
        self.assertEqual(view.ordering_fields, ["flavor_group__name", "name"])

    def test_ordering(self):
        view = FlavorViewSet()
        self.assertEqual(view.ordering, ["flavor_group__name", "name"])


class TestGetSerializerClass(TestCase):
    def test_retrieve(self):
        view = FlavorViewSet()
        view.action = "retrieve"
        self.assertEqual(view.get_serializer_class(), FlavorDetailSerializer)

    def test_list(self):
        view = FlavorViewSet()
        view.action = "list"
        self.assertEqual(view.get_serializer_class(), FlavorSummarySerializer)

    def test_default(self):
        view = FlavorViewSet()
        view.action = "default"
        self.assertEqual(view.get_serializer_class(), FlavorSerializer)
