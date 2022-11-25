from django.shortcuts import render
from profiles.serializers import UserSerializer
from django.contrib.auth.models import User
from core.views import BaseViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from comments.serializers import PostCommentLightSerializer
# from profiles.models import UserMetaInfo
from groups.serializers import GroupInviteReadOnlySerializer, GroupSerializer, MemberRequestSerializer


class ProfileViewSet(BaseViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    serializer_action_classes = {
        'user_comments': PostCommentLightSerializer,
        'requested_groups': MemberRequestSerializer,
        'invitations': GroupInviteReadOnlySerializer,
        'invites': GroupInviteReadOnlySerializer
    }
    permission_action_classes = {
        'requested_groups': [IsAuthenticated,],
        'invitations': [IsAuthenticated,],
        'invites': [IsAuthenticated,],
    }
    search_fields = ['first_name', 'last_name', 'username']
    ordering = ['first_name','last_name']

    @action(detail=False)
    def auth(self, request):
        if request.user.is_authenticated:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
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
                    {"error":"This is your current username. Try another"},
                    status=status.HTTP_409_CONFLICT
                )

            try:
                another_user = User.objects.get(username=new_username)
                return Response(
                    {"error":"This username is taken. Try another"},
                    status=status.HTTP_409_CONFLICT
                )
            except User.DoesNotExist:
                if meta_info is not None:
                    today = datetime.date.today()
                    threshold = today - datetime.timedelta(days=90)
                    if meta_info.username_changed:
                        return Response(
                                {"error": "You can change your username only once."}, status=status.HTTP_409_CONFLICT
                        )
                user.username = new_username
                user.save()
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error":"You are not authorized to change username"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=True, methods=['put'])
    def change_fullname(self, request, username=None):
        user = self.get_object()
        if user == request.user:
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
            try:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return Response({"success": True, "data": request.data}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "success": False, "error": "You are not authorized to change the name"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=True, methods=['post'])
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
                {'success': True,
                'message': "You request for account deletion has been sent. Your account will be deleted in 15 days"}, status=status.HTTP_200_OK
            )
        return Response(
            {'success': False, 'message': "You are not authorized to delete this account."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=True)
    def user_comments(self, request, username=None):
        user = self.get_object()
        if request.user.is_authenticated and hasattr(user, 'postcomment_comments'):
            queryset = user.postcomment_comments.all().order_by('-created_at')
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def requested_groups(self, request, username=None):
        user = self.get_object()
        if user.is_authenticated and hasattr(user, 'requested_groups'):
            queryset = user.requested_groups.all().order_by('-created_at')
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def invitations(self, request, username=None):
        """ Group invites sent by user """

        user = self.get_object()
        if user.is_authenticated and hasattr(user, 'invitations'):
            queryset = user.invitations.all().order_by('-created_at')
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def user_invites(self, request, username=None):
        """ Group invites sent to user """

        user = self.get_object()
        if user.is_authenticated and hasattr(user, 'invites'):
            queryset = user.invites.all().order_by('-created_at')
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class IsAuthenticatedView(APIView):
    def get(self, request):
        if request.user and request.user.is_authenticated:
            fb = {'provider': u'facebook'}
            if request.user.socialaccount_set.count() != 0\
                    and fb in request.user.socialaccount_set\
                    .values('provider'):
                return Response(
                    data={'authenticated': True}, status=status.HTTP_200_OK)
            if not request.user.emailaddress_set\
                    .filter(verified=True).exists():
                return Response(
                    data={'authenticated': False},
                    status=status.HTTP_401_UNAUTHORIZED)
            return Response(
                data={'authenticated': True}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'authenticated': False},
                status=status.HTTP_401_UNAUTHORIZED)
