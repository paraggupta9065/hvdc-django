from django.contrib import admin
from django.urls import include, path
from api.views import PathologyViewSet
from rest_framework.routers import DefaultRouter
from hvdc.views import PingAPIView
from user.views import AddressViewSet, LoginAPIView, NotificationAPIView, PatientViewSet, ProfileAPIView



router = DefaultRouter()
router.register(r'patient', PatientViewSet)
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('notification/', NotificationAPIView.as_view()),
    path('', include(router.urls)),
    
]
