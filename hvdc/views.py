

from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from api.serializers import BannerSerializer, CategorySerializer
from rest_framework.response import Response
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken




class PingAPIView(PublicAPIView):
    def get(self, request):
        return Response({"detail":"Pong, Server Up And Running!"})
    
class LoginAdminAPIView(PublicAPIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(google_id=username).first()
        is_valid = user.check_password(password)
        if(is_valid):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token, 'refresh_token': str(refresh)})
        return Response({"detail":"Wrong Password!"})
        
