
from api.models import Banner, Category, Pathology, PathologyPackage, PathologyTest
from rest_framework import serializers


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
    class Meta:
        model = PathologyTest
        fields = '__all__'

class PathologyPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathologyPackage
        fields = '__all__'
        