from unittest.mock import MagicMock

from django.test import TestCase
from model_bakery import baker
from rest_framework import viewsets

from core.mixins import AutocompleteViewSetMixin
from flavors.models import Flavor


class TestAutocompleteViewSetMixin(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(AutocompleteViewSetMixin, viewsets.GenericViewSet))

    def test_autocomplete_fields(self):
        mixin = AutocompleteViewSetMixin()
        self.assertEqual(mixin.autocomplete_fields, ["id", "name"])

    def test_action(self):
        mixin = AutocompleteViewSetMixin()
        action = mixin.autocomplete
        self.assertEqual(action.url_path, "autocomplete")
        self.assertEqual(list(action.mapping.keys()), ["get"])
        self.assertEqual(action.detail, False)

    def test_autocomplete(self):
        flavor = baker.make(Flavor)
        mixin = AutocompleteViewSetMixin()
        mixin.filter_queryset = MagicMock(return_value=Flavor.objects.all())
        mixin.get_queryset = MagicMock(return_value=Flavor.objects.all())
        response = mixin.autocomplete(None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, {"results": [{"id": flavor.id, "name": flavor.name}]}
        )
