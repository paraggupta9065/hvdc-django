
from django.contrib import admin
from django.urls import include, path
from api.views import BannerView, CartViewSet, CategoryView, PathlogyView, PathologyTestView, PathologyViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'pathologies', PathologyViewSet)
router.register(r'cart', CartViewSet)

urlpatterns = [
    path('user/',  include('user.urls')),
    path('banners/', BannerView.as_view()),
    path('categories/',CategoryView.as_view()),
    path('pathology_test/',PathologyTestView.as_view()),
    path('pathology/',PathlogyView.as_view()),
    path('', include(router.urls)),
]

