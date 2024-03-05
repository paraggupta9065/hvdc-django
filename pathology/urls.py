from django.urls import path, include
from pathology.api.views import PathologyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pathologies', PathologyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
