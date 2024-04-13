import requests
from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from rest_framework.response import Response
from rest_framework import status
from user.models import Address, Notification, Patient, User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.db import transaction

from user.serializers import AddressSerializer, NotificationSerializer, PatientSerializer, UserSerializer





class LoginAPIView(PublicAPIView):
    
    def validateGoogle(self,access_token):
        GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
        response = requests.get(
            GOOGLE_ID_TOKEN_INFO_URL,
            params={'access_token': access_token}
        )
        return response
    def post(self, request):
        try:
            data = request.data
            #Validating From Google's Api        
            response = self.validateGoogle(data["token"])
            if(response.status_code !=200):
                #If Token Is Invalid
                return Response({"detail": "Invalid Token!"}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                response_data = response.json()
                email = response_data["email"]
                id = response_data["sub"]
                user = User.objects.filter(google_id=id,email=email).first()
                if(not user):
                    user =  User.objects.create(
                        name = f'{response_data["name"]} {response_data["family_name"]}',
                        email = response_data["email"],
                        google_id = response_data["sub"],
                        username = response_data["sub"],
                    )
                    
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
class ProfileAPIView(BaseAPIView):
    serializer_class = UserSerializer
    
    def get(self, request):
        try:
                user_data = self.serializer_class(request.user).data
                return Response({'results': user_data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
class NotificationAPIView(BaseAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    
    def get(self, request):
        try:
            data = self.get_queryset();
            notifications = self.serializer_class(data,many=True).data
            return Response({'results': notifications}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PatientViewSet(BaseViewSet):
        queryset = Patient.objects.all()
        serializer_class = PatientSerializer

        def get_queryset(self):
                return self.queryset.filter(created_by=self.request.user)

class AddressViewSet(BaseViewSet):
        queryset = Address.objects.all()
        serializer_class = AddressSerializer

        def get_queryset(self):
                return self.queryset.filter(created_by=self.request.user)