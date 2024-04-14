from rest_framework.decorators import action
from api.models import Banner, Cart, Category, Order, PathologyPackage, PathologyTest, Slot
from common.functions import serailizer_errors
from common.views import BaseAPIView, BaseViewSet, PublicAPIView
from api.serializers import BannerSerializer, CartSerializer, CategorySerializer, OrderSerializer, PathologyPackageSerializer, PathologySerializer, PathologyTestSerializer, SlotSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import Address, Pathology, Patient
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError
from django.db import transaction






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
        return self.queryset
    
    def get(self,request):
        # try:
                self.queryset = self.get_queryset()
                page = self.paginate_queryset(self.queryset,request)
                if page is not None:
                        serializer = self.serializer_class(page, many=True,context={'request': request})
                        return self.get_paginated_response(serializer.data)

                serializer = self.serializer_class(self.queryset, many=True,context={'request': request})
                return Response(serializer.data)
        # except Exception as ex:
        #         print(ex)
        #         raise APIException(detail=ex)


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
                        error_message = serailizer_errors(e)
                        return Response(
                                {"detail": error_message},
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
        @action(detail=False, methods=["post"])
        def remove(self, request, *args, **kwargs):
                try:
                        test_id = request.data.get('test')
                        cart = Cart.objects.get(user=request.user)
                        cart.tests.remove(test_id)
                        
                        if(cart.tests.count()==0):
                                cart.delete()
                                
                        return Response(
                        {"detail": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT
                        )
                except Cart.DoesNotExist as ex:
                        return Response(
                                {"detail": "Cart Does not Exist!"}, status=status.HTTP_404_NOT_FOUND
                        )
                        
                except Exception as ex:
                        raise APIException(detail=ex)


# Pathlogy view
class PathlogyView(BaseAPIView):
    queryset = Pathology.objects.all()
    serializer_class = PathologySerializer

    def get_queryset(self,request):
        is_offline_param = request.query_params.get("is_offline")
            
        if(is_offline_param):
                is_offline = False
                if(is_offline_param == 'true'): is_offline = True
                self.queryset = self.queryset.filter(is_offline=is_offline)
                
        return self.queryset
    
    def get(self,request):
        data =self.serializer_class(self.get_queryset(request=request).all(),many=True)
        return Response({"results":data.data})

class OrderViewSet(BaseViewSet):
        queryset = Order.objects.all()
        serializer_class = OrderSerializer

        def get_queryset(self):
                return self.queryset.filter(user=self.request.user)
        
        def create(self, request, *args, **kwargs):
                try:
                        address = request.data.get("address")
                        patient = request.data.get("patient")
                        
                        with transaction.atomic():
                                user = request.user
                                if(not address or not patient):
                                        raise ValidationError(f"Address Or Patient Is Required!")

                                cart = Cart.objects.get(user=request.user)
                                slot = SlotSerializer(data = request.data)
                                request.data['pathology'] = pathology=cart.tests.all().first().pathology.id
                                slot.is_valid(raise_exception=True)
                                slot = slot.save()
                                
                                order = Order.objects.create(slot =slot ,user=request.user, date_added = cart.date_added,patient = Patient.objects.get(id=patient),address = Address.objects.get(id=address),)
                                order.tests.set(cart.tests.all())
                                order.save()
                                
                                return Response(
                                        {"detail": "Successfully Created!"},
                                        status=status.HTTP_201_CREATED,
                                )
                except Cart.DoesNotExist as e:
                        return Response({"detail": "Cart Not Found !"},status=status.HTTP_400_BAD_REQUEST,)
                        
                except ValidationError as e:
                        error_message = serailizer_errors(e)
                        return Response(
                                {"detail": error_message},
                                status=status.HTTP_400_BAD_REQUEST,
                        )
                except Exception as e:
                        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        # def list(self, request, *args, **kwargs):
        #         try:
        #                 self.queryset = self.filter_queryset(self.get_queryset())
        #                 page = self.paginate_queryset(self.queryset)
        #                 if page is not None:
        #                         serializer = self.get_serializer(page, many=True)
        #                         return self.get_paginated_response(serializer.data)

        #                 serializer = self.get_serializer(self.queryset, many=True)
        #                 return Response(serializer.data)
        #         except Exception as ex:
        #                 raise APIException(detail=ex)
        @action(detail=False, methods=["get"])
        def get_slots(self, request,):
                try:
                        slot_times = [i  for i in range(9,18)]
                        day = request.query_params.get("day")
                        month = request.query_params.get("month")
                        year = request.query_params.get("year")
                        cart = Cart.objects.get(user=request.user)
                        pathology = cart.tests.all().first().pathology
                        current_slots = Slot.objects.filter(pathology=pathology,month=month,day=day,year = year)
                        for current_slot in current_slots:
                                slot_times.remove(current_slot.hour)
                                
                        return Response({"results": {
                                "slots":slot_times,
                                "day":day,
                                "month":month,
                                "year":year,
                        }})
                        pass
                except Cart.DoesNotExist as e:
                        return Response({"detail": "Cart Not Found !"},status=status.HTTP_400_BAD_REQUEST,)
                        
                except ValidationError as e:
                        error_message = serailizer_errors(e)
                        return Response(
                                {"detail": error_message},
                                status=status.HTTP_400_BAD_REQUEST,
                        )
                except Exception as e:
                        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                