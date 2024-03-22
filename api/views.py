
from api.models import Banner, Category, Pathology, PathologyPackage, PathologyTest
from common.views import BaseViewSet, PublicAPIView
from api.serializers import BannerSerializer, CategorySerializer, PathologyPackageSerializer, PathologySerializer, PathologyTestSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view , status

class PathologyViewSet(BaseViewSet):
    queryset = Pathology.objects.all()
    serializer_class = PathologySerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})

class PathologyTestViewSet(BaseViewSet):
    queryset = PathologyTest.objects.all()
    serializer_class = PathologyTestSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})

class PathologyPackageViewSet(BaseViewSet):
    queryset = PathologyPackage.objects.all()
    serializer_class = PathologyPackageSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})


# banner view
class BannerView(PublicAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
       
        

# category view
class CategoryView(PublicAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
            return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset().all(),many=True)
        return Response({"results":data.data})
    


# PathologyTest CRUD 
    
@api_view(['GET', 'POST'])
def pathology_test_list_create(request):
    if request.method == 'GET':
        tests = PathologyTest.objects.all()
        serializer = PathologyTestSerializer(tests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PathologyTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pathology_test_detail(request, pk):
    try:
        test = PathologyTest.objects.get(pk=pk)
    except PathologyTest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PathologyTestSerializer(test)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PathologyTestSerializer(test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
