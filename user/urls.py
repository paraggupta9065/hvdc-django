from django.contrib import admin
from django.urls import include, path
from api.views import PathologyViewSet
from rest_framework.routers import SimpleRouter
from hvdc.views import PingAPIView
from user.views import LoginAPIView



router = SimpleRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    
]

