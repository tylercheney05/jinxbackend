from rest_framework import mixins, viewsets
from sodas.models import Soda
from core.permissions import IsSystemAdminUser
from sodas.serializers import SodaSerializer

class SodaViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    http_method_names = ['get', 'post']
    queryset = Soda.objects.all()
    permission_classes = [IsSystemAdminUser]
    serializer_class = SodaSerializer
    