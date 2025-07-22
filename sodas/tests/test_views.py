from django.test import TestCase
from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from sodas.models import Soda
from sodas.serializers import SodaSerializer
from sodas.views import SodaViewSet


class TestSodaViewSet(TestCase):
    def test_sub_classes(self):
        self.assertTrue(issubclass(SodaViewSet, AutocompleteViewSetMixin))
        self.assertTrue(issubclass(SodaViewSet, viewsets.GenericViewSet))
        self.assertTrue(issubclass(SodaViewSet, mixins.CreateModelMixin))
        self.assertTrue(issubclass(SodaViewSet, mixins.ListModelMixin))

    def test_http_method_names(self):
        view = SodaViewSet()
        self.assertEqual(view.http_method_names, ["get", "post"])

    def test_queryset(self):
        view = SodaViewSet()
        self.assertQuerySetEqual(view.queryset, Soda.objects.all())

    def test_permission_classes(self):
        view = SodaViewSet()
        self.assertEqual(
            view.permission_classes, [IsSystemAdminUserOrIsStaffUserReadOnly]
        )

    def test_serializer_class(self):
        view = SodaViewSet()
        self.assertEqual(view.serializer_class, SodaSerializer)

    def test_autocomplete_fields(self):
        view = SodaViewSet()
        self.assertEqual(view.autocomplete_fields, ["id", "name"])

    def test_filter_backends(self):
        view = SodaViewSet()
        self.assertEqual(view.filter_backends, [filters.OrderingFilter])

    def test_ordering_fields(self):
        view = SodaViewSet()
        self.assertEqual(view.ordering_fields, ["name"])

    def test_ordering(self):
        view = SodaViewSet()
        self.assertEqual(view.ordering, ["name"])
