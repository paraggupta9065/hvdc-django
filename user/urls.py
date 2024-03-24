from django.contrib import admin
from django.urls import include, path
from api.views import PathologyViewSet
from rest_framework.routers import SimpleRouter
from hvdc.views import PingAPIView
from user.views import LoginAPIView, NotificationAPIView, ProfileAPIView



router = SimpleRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('notification/', NotificationAPIView.as_view()),
]

