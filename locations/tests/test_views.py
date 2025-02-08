from django.test import TestCase
from rest_framework import mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from locations.models import Location
from locations.serializers import LocationSerializer
from locations.views import LocationViewSet


class TestLocationViewSet(TestCase):
    def test_sub_classes(self):
        self.assertTrue(issubclass(LocationViewSet, AutocompleteViewSetMixin))
        self.assertTrue(issubclass(LocationViewSet, viewsets.GenericViewSet))
        self.assertTrue(issubclass(LocationViewSet, mixins.CreateModelMixin))
        self.assertTrue(issubclass(LocationViewSet, mixins.ListModelMixin))
        self.assertTrue(issubclass(LocationViewSet, mixins.RetrieveModelMixin))

    def test_http_method_names(self):
        view = LocationViewSet()
        self.assertEqual(view.http_method_names, ["post", "get"])

    def test_model(self):
        view = LocationViewSet()
        self.assertEqual(view.model, Location)

    def test_queryset(self):
        view = LocationViewSet()
        self.assertQuerySetEqual(view.queryset, Location.objects.all())

    def test_permission_classes(self):
        view = LocationViewSet()
        self.assertEqual(
            view.permission_classes, [IsSystemAdminUserOrIsStaffUserReadOnly]
        )

    def test_serializer_class(self):
        view = LocationViewSet()
        self.assertEqual(view.serializer_class, LocationSerializer)

    def test_autocomplete_fields(self):
        view = LocationViewSet()
        self.assertEqual(view.autocomplete_fields, ["id", "name"])
