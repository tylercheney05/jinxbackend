from unittest.mock import MagicMock

from django.test import TestCase
from model_bakery import baker
from rest_framework import mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from cups.models import Cup
from cups.serializers import CupDetailSerializer, CupSerializer, CupSummarySerializer
from cups.views import CupViewSet


class TestCupViewSetBase(TestCase):
    def test_http_method_names(self):
        view = CupViewSet()
        self.assertEqual(view.http_method_names, ["get", "post"])

    def test_model(self):
        view = CupViewSet()
        self.assertEqual(view.model, Cup)

    def test_queryset(self):
        view = CupViewSet()
        self.assertQuerySetEqual(
            view.queryset, Cup.objects.all(), transform=lambda x: x
        )

    def test_permission_classes(self):
        view = CupViewSet()
        self.assertEqual(
            view.permission_classes, [IsSystemAdminUserOrIsStaffUserReadOnly]
        )

    def test_sub_classes(self):
        view = CupViewSet()
        self.assertTrue(issubclass(view.__class__, viewsets.GenericViewSet))
        self.assertTrue(issubclass(view.__class__, mixins.CreateModelMixin))
        self.assertTrue(issubclass(view.__class__, mixins.ListModelMixin))
        self.assertTrue(issubclass(view.__class__, mixins.RetrieveModelMixin))
        self.assertTrue(issubclass(view.__class__, AutocompleteViewSetMixin))


class TestCupViewSetGetSerializerClass(TestCase):
    def test_retrieve(self):
        view = CupViewSet()
        view.action = "retrieve"
        self.assertEqual(view.get_serializer_class(), CupDetailSerializer)

    def test_list(self):
        view = CupViewSet()
        view.action = "list"
        self.assertEqual(view.get_serializer_class(), CupSummarySerializer)

    def test_default(self):
        view = CupViewSet()
        view.action = "default"
        self.assertEqual(view.get_serializer_class(), CupSerializer)


class TestCupViewSetAutocomplete(TestCase):
    def test_autocomplete(self):
        cup = baker.make(Cup)
        request = MagicMock()

        view = CupViewSet(request=request)
        response = view.autocomplete(None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"results": [{"id": cup.id, "size__display": f"{cup.size} oz"}]},
        )
