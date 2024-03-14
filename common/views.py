import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


# for the banner 
from rest_framework import generics
from hvdc.serializers import BannerSerializer





from common.pagination import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from common.permissions import (
    IsActiveUser,
    IsSuperAdmin,
    IsAdminOrSuperAdminOrEditor,
    IsAdminOrSuperAdmin,
)
from common.functions import serailizer_errors

CACHE_INTERVAL = 0

logger = logging.getLogger(__name__)


class BaseViewSet(ModelViewSet):
    pagination = True
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update"]:
            permission_classes = [IsAdminOrSuperAdminOrEditor]
        else:
            permission_classes = [IsAdminOrSuperAdmin]

        permission_classes += [IsActiveUser]

        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(CACHE_INTERVAL, cache="default"))
    def dispatch(self, request, *args, **kwargs):
        return super(BaseViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter objects based on the user (current user)
        user = self.request.user
        if self.request.user.role == "superadmin":
            return self.queryset.filter(created_by=user)
        else:
            return self.queryset.filter(users__in=[user])

    def get_serializer_context(self):
        """
        Passing the request to serializers in context.
        """
        context = super(BaseViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        try:
            self.queryset = self.filter_queryset(self.get_queryset()).order_by("-created_on")

            if self.pagination:
                page = self.paginate_queryset(self.queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data)
        except Exception as ex:
            logger.info("Something went wrong", exc_info=ex)
            raise APIException(detail=ex)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user requesting the delete has the necessary permission
        if instance.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to delete this object.")

        instance.delete()
        return Response(
            {"detail": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            # Check if the user requesting the update has the necessary permission
            if instance.created_by != self.request.user:
                raise PermissionDenied(
                    "You don't have permission to update this object."
                )

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        except ValidationError as e:
            field_name, error_message = serailizer_errors(e)
            return Response(
                {"detail": f"{field_name} - {error_message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != self.request.user:
            raise PermissionDenied("You don't have permission to access this object.")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Set the created_by field to the current user before saving
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return Response(
                {"detail": "Successfully Created!"},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except ValidationError as e:
            field_name, error_message = serailizer_errors(e)
            return Response(
                {"detail": f"{field_name} - {error_message}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BaseAPIView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ["GET", "HEAD"]:
            permission_classes = [IsAuthenticated]
        elif self.request.method in ["PUT", "HEAD"]:
            permission_classes = [IsAdminOrSuperAdminOrEditor]
        else:
            permission_classes = [IsAdminOrSuperAdmin]
        permission_classes += [IsActiveUser]
        return [permission() for permission in permission_classes]


class PublicAPIView(APIView):
    permission_classes = [AllowAny]


