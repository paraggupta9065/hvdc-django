from rest_framework import serializers
from pathology.models import Pathology

class PathologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathology
        fields = '__all__'
