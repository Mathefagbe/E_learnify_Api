from django.urls import path as url ,re_path 
from .views import (UserRegistrationApiView,
                    ResetPasswordApiView,
                    # EmailConfirmationView,
                    PhoneNumberVerificationApiView,
                    LoginApiView, 
                    socialAuthentication,
                    # UserInputPhoneNumberApiView
                    )
from rest_framework_simplejwt.views import (TokenRefreshView,
                                            TokenBlacklistView)


urlpatterns = [
    url('auth/create/account/',UserRegistrationApiView.as_view(),name='create_account'),
    url('auth/verify/phone-number/',PhoneNumberVerificationApiView.as_view(),name='verify_phone_number'),
    url('auth/reset/password/',ResetPasswordApiView.as_view(),name='reset_password'),
    url('auth/sign-in/',LoginApiView.as_view(), name="sign_in"),
    url('auth/token/refresh/',TokenRefreshView.as_view(), name="token_obtain_pair"),
    url('auth/logout/',TokenBlacklistView.as_view(),name='logout'),
    re_path('auth/' + r'social/(?P<backend>[^/]+)/$', socialAuthentication),
]


    # url('auth/create/account/phone_number/',UserInputPhoneNumberApiView.as_view(),name='create_account_phonenumber'),
    # url('auth/confirm-email/<uid>/<token>',EmailConfirmationView.as_view(),name='verify_email'),
    # re_path('auth/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', socialAuthentication),