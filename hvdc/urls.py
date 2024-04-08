from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from hvdc.views import LoginAdminAPIView, PingAPIView
from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static


router = SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginAdminAPIView.as_view()),
    path('', PingAPIView.as_view()),
    path('api/', include('api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

