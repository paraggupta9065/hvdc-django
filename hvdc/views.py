

from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from hvdc.serializers import BannerSerializer, CategorySerializer, PharmacySerializer
from pathology.models import Banner, Category_model, Pharmacy
from rest_framework.response import Response



class PingAPIView(PublicAPIView):
    def get(self, request):
        return Response({"detail":"Server Up And Running!"})
    

# banner view
class BannerListsView(PublicAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
       
        

# category view
class CategoryListView(PublicAPIView):
    queryset = Category_model.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
    

# Pharmacy view 
class PharmacyListView(PublicAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
     