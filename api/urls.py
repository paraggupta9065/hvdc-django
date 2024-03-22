
from django.contrib import admin
from django.urls import include, path
from api.views import BannerView, CategoryView, PathologyViewSet
from rest_framework.routers import DefaultRouter
from .views import pathology_test_list_create, pathology_test_detail

router = DefaultRouter()
router.register(r'pathologies', PathologyViewSet)

urlpatterns = [
    path('user/',  include('user.urls')),
    path('banners/', BannerView.as_view()),
    path('categories/',CategoryView.as_view()),
    path('', include(router.urls)),
    path('pathologytests/', pathology_test_list_create, name='pathologytest-list-create'),
    path('pathologytests/<int:pk>/', pathology_test_detail, name='pathologytest-detail'),
]

