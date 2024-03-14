from common.views import BaseViewSet
from rest_framework import viewsets
from pathology.models import Pathology
from pathology.serializers.pathology import PathologySerializer

class PathologyViewSet(BaseViewSet):
    queryset = Pathology.objects.all()
    serializer_class = PathologySerializer
    lookup_field = 'uuid'