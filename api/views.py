
from api.models import Banner, Category, PathologyPackage, PathologyTest
from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from api.serializers import BannerSerializer, CategorySerializer, PathologyPackageSerializer, PathologySerializer, PathologyTestSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import Pathology
from django.db.models import Q

class PathologyViewSet(BaseViewSet):
    queryset = Pathology.objects.all()
    serializer_class = PathologySerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})

class PathologyTestView(BaseAPIView):
    queryset = PathologyTest.objects.all()
    serializer_class = PathologyTestSerializer
    
    def get_queryset(self):
        
        search_term = self.request.query_params.get("key")
        if(search_term):
                self.queryset = self.queryset.filter(
                        Q(name__icontains=search_term) | 
                        Q(description__icontains=search_term) |  
                        Q(test_type__icontains=search_term) |  
                        Q(category__category_name__icontains=search_term)  
                )
        category_id = self.request.query_params.get("category")
        if(category_id):
                print(category_id)
                self.queryset = self.queryset.filter(
                     category = category_id
                )
        pathology_id = self.request.query_params.get("pathology")
        if(pathology_id):
                self.queryset = self.queryset.filter(
                     pathology = pathology_id
                )
        is_offline = self.request.query_params.get("is_offline")
        if(is_offline):
                self.queryset = self.queryset.filter(
                     is_offline = is_offline
                )
        return self.queryset.all()
    
    def get(self,request):
        queryset_data = self.get_queryset()
        db_data =self.serializer_class(queryset_data,many=True)
        return Response({"results":db_data.data})

class PathologyPackageViewSet(BaseViewSet):
    queryset = PathologyPackage.objects.all()
    serializer_class = PathologyPackageSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})


# banner view
class BannerView(BaseAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
       
        

# category view
class CategoryView(BaseAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
    

