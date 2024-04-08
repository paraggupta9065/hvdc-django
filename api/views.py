
from api.models import Banner, Cart, Category, PathologyPackage, PathologyTest
from common.functions import serailizer_errors
from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from api.serializers import BannerSerializer, CartSerializer, CategorySerializer, PathologyPackageSerializer, PathologySerializer, PathologyTestSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import Pathology
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError





class PathologyViewSet(BaseViewSet):
    queryset = Pathology.objects.all()
    serializer_class = PathologySerializer
    
    def get_queryset(self):
            return self.queryset


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
        db_data =self.serializer_class(queryset_data,many=True,context={'request': request})
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
    
# cart view                
class CartViewSet(BaseViewSet):
        queryset = Cart.objects.all()
        serializer_class = CartSerializer

        def get_queryset(self):
                return self.queryset
        
        def validate_test(self,cart,test_id):
                tests= cart.tests.all()
                if(tests.count()==0):
                        return True
                current_test = tests.first()
                try:
                        test = PathologyTest.objects.get(id=test_id)
                except:
                        raise ValidationError(f"Test Not Found !")
                if(current_test.pathology==test.pathology and current_test.is_offline!=test.is_offline):
                        raise ValidationError(f"Previous Test in Your Cart Is {current_test.is_offline} Please Add Same Test Or Clear Cart !")
                
                return (current_test.pathology==test.pathology)
        def create(self, request,):
                try:
                        test_id = request.data.get('test')
                        
                        if(not test_id):
                                raise ValidationError("Test Id Not Found!")
                                
                        try:
                                cart = Cart.objects.get(user=request.user)
                        except:
                                cart = Cart.objects.create(user=request.user)
                                
                        
                        valid = self.validate_test(cart,test_id)
                        
                        if(valid==True):
                                cart.tests.add(test_id)
                                return Response({"detail":"Test added in cart!"},    status=status.HTTP_200_OK,)
                        else:
                                return valid
                except ValidationError as e:
                        field_name, error_message = serailizer_errors(e)
                        return Response(
                                {"detail": f"{field_name} - {error_message}"},
                                status=status.HTTP_400_BAD_REQUEST,
                        )
                except Exception as ex:
                        raise APIException(detail=ex)
        def list(self, request, *args, **kwargs):
                try:
                        user = self.request.user
                        cart = Cart.objects.get(user=request.user)
                        cart_total = cart.total_price()
                        
                        serializer = self.get_serializer(cart)
                        return Response({"results":{
                                "cart":serializer.data,
                                "cart_total":cart_total,
                                
                        }})
                except Cart.DoesNotExist as ex:
                        return Response(
                                {"detail": "Cart Does not Exist!"}, status=status.HTTP_404_NOT_FOUND
                        )
                        
                except Exception as ex:
                        raise APIException(detail=ex)