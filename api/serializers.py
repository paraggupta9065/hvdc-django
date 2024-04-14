
from api.models import Banner, Cart, Category, Order, PathologyPackage, PathologyTest, Slot
from rest_framework import serializers
from user.models import Pathology
from rest_framework.fields import CurrentUserDefault
from user.serializers import AddressSerializer, PatientSerializer

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class PathologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathology
        fields = '__all__'

class PathologyTestSerializer(serializers.ModelSerializer):
    in_cart = serializers.SerializerMethodField()

    def get_in_cart(self, obj):
        user = self.context.get("request").user
        cart = Cart.objects.filter(user=user).first()
        if(not cart):
            return False
        return obj in cart.tests.all();
    class Meta:
        model = PathologyTest
        fields = '__all__'

class PathologyPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathologyPackage
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    tests = PathologyTestSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = '__all__'
        
        
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    tests = PathologyTestSerializer(many=True)
    address = AddressSerializer()
    patient = PatientSerializer()
    slot = SlotSerializer()
    
    def total_price(self):
        total = 0
        for test in self.tests.all():
            total += test.price
        return total
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price']=instance.total_price()
        return representation
    class Meta:
        model = Order
        fields = '__all__'
