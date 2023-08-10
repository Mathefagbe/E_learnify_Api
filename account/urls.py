from django.urls import path as url ,re_path 
from .views import (UserRegistrationApiView,
                    ResetPasswordApiView,
                    EmailVerificationApiView,
                    ForgetPasswordEmailVerificationApiView,
                    LoginApiView, socialAuthentication
                    )
from rest_framework_simplejwt.views import (TokenRefreshView,TokenBlacklistView)


urlpatterns = [
    url('auth/create/account/',UserRegistrationApiView.as_view(),name='create_account'),
    url('auth/verify/account/',EmailVerificationApiView.as_view(),name='verify_account'),
    url('auth/verify/forgetpassword/',ForgetPasswordEmailVerificationApiView.as_view(),name='verify_forgetpassword'),
    url('auth/reset/password/',ResetPasswordApiView.as_view(),name='reset_password'),
    # url("auth/sign_in/",LoginApiView.as_view(),name="sign_in"),
    url('auth/sign_in/',LoginApiView.as_view(), name="sign_in"),
    url('auth/token/refresh/',TokenRefreshView.as_view(), name="token_obtain_pair"),
    url('auth/logout/',TokenBlacklistView.as_view(),name='logout'),
    re_path('auth/' + r'social/(?P<backend>[^/]+)/$', socialAuthentication),
    # re_path('auth/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', socialAuthentication),
]