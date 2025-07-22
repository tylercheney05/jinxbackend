from django.test import TestCase
from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from menus.models import Menu
from menus.serializers import MenuSerializer
from menus.views import MenuViewSet


class TestMenuViewSet(TestCase):
    def test_sub_classes(self):
        self.assertTrue(issubclass(MenuViewSet, viewsets.GenericViewSet))
        self.assertTrue(issubclass(MenuViewSet, mixins.CreateModelMixin))
        self.assertTrue(issubclass(MenuViewSet, mixins.ListModelMixin))

    def test_http_method_names(self):
        view = MenuViewSet()
        self.assertEqual(view.http_method_names, ["post", "get"])

    def test_queryset(self):
        view = MenuViewSet()
        self.assertQuerySetEqual(view.queryset, Menu.objects.all())

    def test_permission_classes(self):
        view = MenuViewSet()
        self.assertEqual(
            view.permission_classes, [IsSystemAdminUserOrIsStaffUserReadOnly]
        )

    def test_serializer_class(self):
        view = MenuViewSet()
        self.assertEqual(view.serializer_class, MenuSerializer)
