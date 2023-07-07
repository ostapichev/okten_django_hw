from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.views import ActivateUserView, MeView, RecoveryPasswordRequestView, RecoveryPasswordView

urlpatterns = [
    path('', TokenObtainPairView.as_view()),
    path('/activate/<str:token>', ActivateUserView.as_view()),
    path('/refresh', TokenRefreshView.as_view()),
    path('/recovery_password', RecoveryPasswordRequestView.as_view()),
    path('/recovery_password/<str:token>', RecoveryPasswordView.as_view()),
    path('/me', MeView.as_view()),
]