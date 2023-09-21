from django.urls import path
from rest_framework_simplejwt.views import (TokenVerifyView,
                                            TokenRefreshView,
                                            TokenBlacklistView)
from .views import (SignUpView,
                    LoginView,
                    VerifyEmailView,
                    LoginWithGoogleView,
                    IsAuthenticatedView,
                    GoogleExchangeCodeForTokenView,
                    get_calender_events)

urlpatterns = [
    # endpoint to verify the token
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

    # endpoints for login and signup
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('email-verification/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='token_login'),
    path('google-login/', LoginWithGoogleView.as_view() , name='google_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # testing endpoints
    path('exchange_code_for_token/', GoogleExchangeCodeForTokenView.as_view(),
        name='exchange_code_for_token'),
    path('is-authenticated/', IsAuthenticatedView.as_view(),
        name='is_authenticated'),
    path('events/', get_calender_events, name='get_calender_events'),


]
