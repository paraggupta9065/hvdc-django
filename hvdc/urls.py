from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from hvdc.views import BannerListsView, PingAPIView

router = SimpleRouter()



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PingAPIView.as_view()),
    path('api/user/',  include('user.urls')),
    path('api/pathology/',  include('pathology.urls')),
    path('api/banners/', BannerListsView.as_view()),
]

