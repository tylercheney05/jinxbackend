from django.test import TestCase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from menuitems.models import LimitedTimePromotion
from menuitems.serializers.limited_time_promotion import LimitedTimePromotionSerializer
from menuitems.views import LimitedTimePromotionViewSet


class TestLimitedTimePromotionViewSet(TestCase):
    def test_sub_classes(self):
        self.assertTrue(
            issubclass(LimitedTimePromotionViewSet, AutocompleteViewSetMixin)
        )
        self.assertTrue(
            issubclass(LimitedTimePromotionViewSet, mixins.CreateModelMixin)
        )
        self.assertTrue(issubclass(LimitedTimePromotionViewSet, mixins.ListModelMixin))
        self.assertTrue(
            issubclass(LimitedTimePromotionViewSet, mixins.UpdateModelMixin)
        )

    def test_http_method_names(self):
        view = LimitedTimePromotionViewSet()
        self.assertEqual(view.http_method_names, ["post", "get", "put"])

    def test_model(self):
        view = LimitedTimePromotionViewSet()
        self.assertEqual(view.model, LimitedTimePromotion)

    def test_queryset(self):
        view = LimitedTimePromotionViewSet()
        self.assertQuerySetEqual(view.queryset, view.model.objects.all())

    def test_permission_classes(self):
        view = LimitedTimePromotionViewSet()
        self.assertEqual(
            view.permission_classes, [IsSystemAdminUserOrIsStaffUserReadOnly]
        )

    def test_serializer_class(self):
        view = LimitedTimePromotionViewSet()
        self.assertEqual(view.serializer_class, LimitedTimePromotionSerializer)

    def test_filter_backends(self):
        view = LimitedTimePromotionViewSet()
        self.assertEqual(view.filter_backends, [DjangoFilterBackend])

    def test_filterset_fields(self):
        view = LimitedTimePromotionViewSet()
        self.assertEqual(view.filterset_fields, ["is_archived"])
