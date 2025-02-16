from unittest.mock import MagicMock, patch

from django.test import TestCase
from django_filters.rest_framework import DjangoFilterBackend
from model_bakery import baker
from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from flavors.models import Flavor
from menuitems.filters import MenuItemFilter
from menuitems.models import LimitedTimePromotion, MenuItem
from menuitems.serializers.menu_item import (
    MenuItemDetailSerializer,
    MenuItemSerializer,
    MenuItemSummarySerializer,
)
from menuitems.views import MenuItemViewSet
from sodas.models import Soda


class TestMenuItemViewSet(TestCase):
    def test_sub_classes(self):
        self.assertTrue(issubclass(MenuItemViewSet, viewsets.GenericViewSet))
        self.assertTrue(issubclass(MenuItemViewSet, mixins.CreateModelMixin))
        self.assertTrue(issubclass(MenuItemViewSet, mixins.ListModelMixin))
        self.assertTrue(issubclass(MenuItemViewSet, mixins.RetrieveModelMixin))

    def test_http_method_name(self):
        view = MenuItemViewSet()
        self.assertEqual(view.http_method_names, ["post", "get"])

    def test_model(self):
        view = MenuItemViewSet()
        self.assertEqual(view.model, MenuItem)

    def test_queryset(self):
        view = MenuItemViewSet()
        self.assertQuerySetEqual(view.queryset, view.model.objects.all())

    def test_permission_classes(self):
        view = MenuItemViewSet()
        self.assertEqual(
            view.permission_classes, [IsSystemAdminUserOrIsStaffUserReadOnly]
        )

    def test_filter_backends(self):
        view = MenuItemViewSet()
        self.assertEqual(view.filter_backends, [DjangoFilterBackend])

    def test_filterset_class(self):
        view = MenuItemViewSet()
        self.assertEqual(view.filterset_class, MenuItemFilter)


class TestGetSerializerClass(TestCase):
    def test_get_serializer_class_retrieve(self):
        view = MenuItemViewSet()
        view.action = "retrieve"
        self.assertEqual(view.get_serializer_class(), MenuItemDetailSerializer)

    def test_get_serializer_class_list(self):
        view = MenuItemViewSet()
        view.action = "list"
        self.assertEqual(view.get_serializer_class(), MenuItemSummarySerializer)

    def test_get_serializer_class_default(self):
        view = MenuItemViewSet()
        view.action = "default"
        self.assertEqual(view.get_serializer_class(), MenuItemSerializer)
