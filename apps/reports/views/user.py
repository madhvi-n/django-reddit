from core.views import BaseReadOnlyViewSet, BaseViewSet
from django.contrib.auth.models import User
from reports.models import UserProfileReport
from reports.serializers import (
    UserProfileReportLightSerializer,
    UserProfileReportSerializer,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserProfileReportPagination(PageNumberPagination):
    page_size = 24


class UserProfileReportViewSet(BaseViewSet):
    queryset = UserProfileReport.objects.all()
    pagination_class = UserProfileReportPagination
    serializer_class = UserProfileReportSerializer
    serializer_action_classes = {
        "retrieve": UserProfileReportLightSerializer,
        "redact": UserProfileReportLightSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs != {}:
            if "user_username" in self.kwargs:
                return self.queryset.filter(
                    reported_user__username=self.kwargs["user_username"]
                )
        return queryset

    def create(self, request, user_username=None):
        data = request.data
        if not request.user.is_authenticated:
            return Response(
                {"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if data["reporter"] != request.user.pk:
            return Response(
                {"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN
            )
        if user_username is not None:
            try:
                data["reported_user"] = User.objects.get(username=user_username).pk
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "Wrong Username"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Error in route"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, user_username=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, user_username=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, user_username=None, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["put"])
    def redact(self, request, user_username=None, pk=None):
        report = self.get_object()
        if not request.user.is_authenticated:
            return Response(
                {"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if report.reporter.pk != request.user.pk:
            return Response(
                {"error": "Spoofing detected"}, status=status.HTTP_403_FORBIDDEN
            )
        report.status = UserProfileReport.STATUS.REDACTED.value
        report.save()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
