from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pathology.models import Pathology
from pathology.serializers.pathology import PathologySerializer

class PathologyList(APIView):
    def get(self, request):
        pathologies = Pathology.objects.all()
        serializer = PathologySerializer(pathologies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PathologySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PathologyDetail(APIView):
    def get_object(self, uuid):
        try:
            return Pathology.objects.get(uuid=uuid)
        except Pathology.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uuid):
        pathology = self.get_object(uuid)
        serializer = PathologySerializer(pathology)
        return Response(serializer.data)

    def put(self, request, uuid):
        pathology = self.get_object(uuid)
        serializer = PathologySerializer(pathology, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        pathology = self.get_object(uuid)
        pathology.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
