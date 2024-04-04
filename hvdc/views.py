

from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from api.serializers import BannerSerializer, CategorySerializer
from rest_framework.response import Response



class PingAPIView(PublicAPIView):
    def get(self, request):
        return Response({"detail":"Pong, Server Up And Running!"})
    
