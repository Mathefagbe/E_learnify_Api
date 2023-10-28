import string,datetime
from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import PhoneNumberVerification
from django.contrib.auth import get_user_model
from utils.error_handler import error_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError,AuthenticationFailed



User=get_user_model()


@staticmethod
def check_verification(user):
    # try:
          if not user.is_verified:
               raise serializers.ValidationError({"detail":"A Verification link has been sent to your email"})


@staticmethod
def check_isactive(user):
     if not User.is_active:
          raise serializers.ValidationError('You account have been disabled')
     

    

@staticmethod
def jwt_token(user):
    data={}
    refresh=RefreshToken.for_user(user)   
    data["refresh"] = str(refresh)
    data["access"] = str(refresh.access_token)
    return data
