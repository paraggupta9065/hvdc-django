

from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from hvdc.serializers import BannerSerializer
from pathology.models import Banner
from rest_framework.response import Response



class PingAPIView(PublicAPIView):
    def get(self, request):
        return Response({"detail":"Server Up And Running!"})
    

class BannerListsView(PublicAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
       
        
        