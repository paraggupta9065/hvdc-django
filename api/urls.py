
from django.contrib import admin
from django.urls import include, path
from api.views import BannerView, CategoryView, PathologyViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'pathologies', PathologyViewSet)

urlpatterns = [
    path('user/',  include('user.urls')),
    path('banners/', BannerView.as_view()),
    path('categories/',CategoryView.as_view()),
    path('', include(router.urls)),
    
]

