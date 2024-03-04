from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from hvdc.views import PingAPIView
from user.views import LoginAPIView

router = SimpleRouter()



urlpatterns = [
    path('login/', LoginAPIView.as_view()),
]

