import pandas as pd
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AutocompleteViewSetMixin(viewsets.GenericViewSet):
    autocomplete_fields = ["id", "name"]

    @action(detail=False, methods=["get"], url_path="autocomplete")
    def autocomplete(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        df = pd.DataFrame(queryset.values(*self.autocomplete_fields))
        return Response({"results": df.to_dict("records")})
