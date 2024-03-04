

from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from rest_framework.response import Response



class LoginAPIView(PublicAPIView):
    def get(self, request):
        return Response({"detail":"Login Sucess!"})