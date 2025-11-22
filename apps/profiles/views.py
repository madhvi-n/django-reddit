from bookmarks.models import PostBookmark
from bookmarks.serializers import PostBookmarkReadOnlySerializer
from comments.serializers import PostCommentLightSerializer, PostCommentVoteSerializer
from core.views import BaseViewSet
from django.contrib.auth.models import User
from django.shortcuts import render
from groups.serializers import (
    GroupInviteReadOnlySerializer,
    GroupSerializer,
    MemberRequestSerializer,
)
from posts.serializers import PostVoteHeavySerializer
from profiles.serializers import UserSerializer
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileViewSet(BaseViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserSerializer
    serializer_action_classes = {
        "user_comments": PostCommentLightSerializer,
        "requested_groups": MemberRequestSerializer,
        "invitations": GroupInviteReadOnlySerializer,
        "invites": GroupInviteReadOnlySerializer,
        "user_upvotes": PostVoteHeavySerializer,
        "bookmarks": PostBookmarkReadOnlySerializer,
    }
    permission_action_classes = {
        "requested_groups": [
            IsAuthenticated,
        ],
        "invitations": [
            IsAuthenticated,
        ],
        "invites": [
            IsAuthenticated,
        ],
        "bookmarks": [IsAuthenticated],
    }
    search_fields = ["first_name", "last_name", "username"]
    ordering = ["first_name", "last_name"]

    @action(detail=False)
    def auth(self, request):
        if request.user.is_authenticated:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["put"])
    def change_username(self, request, username=None):
        user = self.get_object()
        if user == request.user:
            meta_info = None
            try:
                meta_info = UserMetaInfo.objects.get(user=user)
            except UserMetaInfo.DoesNotExist:
                pass

            new_username = request.data["new_username"]
            if user.username == new_username:
                return Response(
                    {"error": "This is your current username. Try another"},
                    status=status.HTTP_409_CONFLICT,
                )

            try:
                another_user = User.objects.get(username=new_username)
                return Response(
                    {"error": "This username is taken. Try another"},
                    status=status.HTTP_409_CONFLICT,
                )
            except User.DoesNotExist:
                if meta_info is not None:
                    today = datetime.date.today()
                    threshold = today - datetime.timedelta(days=90)
                    if meta_info.username_changed:
                        return Response(
                            {"error": "You can change your username only once."},
                            status=status.HTTP_409_CONFLICT,
                        )
                user.username = new_username
                user.save()
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "You are not authorized to change username"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(detail=True, methods=["put"])
    def change_fullname(self, request, username=None):
        user = self.get_object()
        if user == request.user:
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
            try:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return Response(
                    {"success": True, "data": request.data}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"success": False, "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"success": False, "error": "You are not authorized to change the name"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, username=None):
        user = self.get_object()
        if user == request.user:
            user.is_active = False
            user.save()
        return Response({"message": "Account Deactivated"}, status=status.HTTP_200_OK)

    def destroy(self, request, username=None):
        user = self.get_object()
        if user == request.user:
            user.is_requesting_delete = True
            user.save()
            return Response(
                {
                    "success": True,
                    "message": "You request for account deletion has been sent. Your account will be deleted in 15 days",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "You are not authorized to delete this account.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(detail=True)
    def user_comments(self, request, username=None):
        user = self.get_object()
        if hasattr(user, "postcomment_comments"):
            queryset = user.postcomment_comments.all().order_by("-created_at")
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def requested_groups(self, request, username=None):
        user = self.get_object()
        if user.is_authenticated and hasattr(user, "requested_groups"):
            queryset = user.requested_groups.all().order_by("-created_at")
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def invitations(self, request, username=None):
        """Group invites sent by user"""
        user = self.get_object()
        if user.is_authenticated and hasattr(user, "invitations"):
            queryset = user.invitations.all().order_by("-created_at")
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def user_invites(self, request, username=None):
        """Group invites sent to user"""
        user = self.get_object()
        if user.is_authenticated and hasattr(user, "invites"):
            queryset = user.invites.all().order_by("-created_at")
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def _common_vote_method(self, request, user_vote):
        user = self.get_object()
        post_queryset = (
            user.post_votes.all().order_by("-created_at").filter(vote=user_vote)
        )
        comment_queryset = (
            user.postcommentvote_votes.all()
            .order_by("-created_at")
            .filter(vote=user_vote)
        )
        post_serializer = PostVoteHeavySerializer(post_queryset, many=True)
        comment_serializer = PostCommentVoteSerializer(comment_queryset, many=True)
        return Response(
            {"posts": post_serializer.data, "comments": comment_serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True)
    def user_upvotes(self, request, username=None):
        """Returns user upvoted posts and comments"""
        return self._common_vote_method(request, 1)

    @action(detail=True)
    def user_downvotes(self, request, username=None):
        """Returns user downvoted posts and comments"""
        return self._common_vote_method(request, -1)

    @action(detail=True)
    def bookmarks(self, request, username=None):
        """Returns user bookmarks"""
        user = self.get_object()
        if user.is_authenticated:
            queryset = PostBookmark.objects.filter(
                user__username=user.username
            ).order_by("-created_at")
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class IsAuthenticatedView(APIView):
    def get(self, request):
        if request.user and request.user.is_authenticated:
            fb = {"provider": "facebook"}
            if (
                request.user.socialaccount_set.count() != 0
                and fb in request.user.socialaccount_set.values("provider")
            ):
                return Response(data={"authenticated": True}, status=status.HTTP_200_OK)
            if not request.user.emailaddress_set.filter(verified=True).exists():
                return Response(
                    data={"authenticated": False}, status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(data={"authenticated": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"authenticated": False}, status=status.HTTP_401_UNAUTHORIZED
            )
