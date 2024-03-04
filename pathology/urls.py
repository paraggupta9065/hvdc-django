from django.urls import path
from pathology.api.Pathology import PathologyList, PathologyDetail

urlpatterns = [
    path('pathologies/', PathologyList.as_view(), name='pathology-list'),
    path('pathologies/<uuid:uuid>/', PathologyDetail.as_view(), name='pathology-detail'),
]
