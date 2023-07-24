from django.urls import path

from .views import (
    ActivateEmail,
    AdminToUserView,
    BlockAdminUserView,
    BlockUserView,
    UnBlockAdminUserView,
    UnBlockUserView,
    UserAddAvatarView,
    UserListCreateView,
    UserToAdminView,
)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='users_list_create'),
    path('/avatar', UserAddAvatarView.as_view(), name='user_avatar_view'),
    path('/<int:pk>/to_admin', UserToAdminView.as_view(), name='user_to_admin'),
    path('/<int:pk>/to_user', AdminToUserView.as_view(), name='admin_to_user'),
    path('/<int:pk>/block_user', BlockUserView.as_view(), name='block_user'),
    path('/<int:pk>/un_block_user', UnBlockUserView.as_view(), name='un_block_user'),
    path('/<int:pk>/block_admin', BlockAdminUserView.as_view(), name='block_admin'),
    path('/<int:pk>/un_block_admin', UnBlockAdminUserView.as_view(), name='un_block_admin'),
    path('/email', ActivateEmail.as_view(), name='activate_email')
]
