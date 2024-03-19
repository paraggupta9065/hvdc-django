from django.contrib import admin
from django.urls import include, path
from hvdc.views import PingAPIView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PingAPIView.as_view()),
    path('api/', include('api.urls')),

]

