from django.urls import path
from rest_framework_simplejwt.views import (TokenVerifyView,
                                            TokenRefreshView, 
                                            TokenBlacklistView)
from .views import SignUpView, LoginView, VerifyEmailView

urlpatterns = [
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('email-verification/', VerifyEmailView.as_view(), name='verify_email'),
    path('login', LoginView.as_view(), name='token_login'),

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

