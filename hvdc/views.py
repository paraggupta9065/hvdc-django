

from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from rest_framework.response import Response



class PingAPIView(PublicAPIView):
    def get(self, request):
        return Response({"detail":"Server Up And Running!"})