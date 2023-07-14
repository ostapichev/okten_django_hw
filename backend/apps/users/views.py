from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permission import IsAdminOrWriteOnlyPermission, IsSuperUser
from core.services.email_service import EmailService

from .filters import UserFilter
from .models import UserModel as User
from .serializers import AvatarSerializer, UserSerializer

UserModel: User = get_user_model()


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class UserListCreateView(ListCreateAPIView):
    """
        get:
            Get all users
        post:
            Creation an users
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    filterset_class = UserFilter
    permission_classes = (IsAdminOrWriteOnlyPermission,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)


class UserAddAvatarView(UpdateAPIView):
    """
        Add an avatar to a user
    """
    serializer_class = AvatarSerializer
    http_method_names = ('put',)

    def get_object(self):
        return UserModel.objects.all_with_profiles().get(pk=self.request.user.pk).profile

    def perform_update(self, serializer):
        self.get_object().avatar.delete()
        super().perform_update(serializer)


class UserToAdminView(GenericAPIView):
    """
        Add administrator rights to the user
    """
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    """
        Revoke administrator rights from a user
    """
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(GenericAPIView):
    """
        Block user
    """
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(GenericAPIView):
    """
        Unblock user
    """
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockAdminUserView(BlockUserView):
    """
        Block Admin
    """
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()


class UnBlockAdminUserView(UnBlockUserView):
    """
        Unblock Admin
    """
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()


class ActivateEmail(GenericAPIView):
    """
        Send email to activate user
    """
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        EmailService.test_email()
        return Response('ok')