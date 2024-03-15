
from pathology.models import Banner, Pharmacy
from rest_framework import serializers
from pathology.models import Category_model


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_model
        fields = '__all__'
        
        

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy 
        fields = '__all__'

