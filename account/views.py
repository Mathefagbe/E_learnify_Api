from typing import Any
from django.shortcuts import get_object_or_404
from django import http
from rest_framework.generics import CreateAPIView
from .services import jwt_token
from.serializers import (UserInputSerializer,
                         PhoneNumberVerifyInputSerialzer,
                         ForgetPasswordInputSerializer,)
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework import status
from django.contrib.auth import get_user_model
from utils.error_handler import error_handler
from rest_framework_simplejwt.views import (TokenObtainPairView)
from rest_framework.exceptions import AuthenticationFailed
from social_django.utils import psa
from rest_framework.decorators import api_view,permission_classes
# from django.views.generic import TemplateView
# from utils.converter import bytes_Converter
from .mixin import UserCreateMixin,PhoneNumberVerificationMixin



user=get_user_model()
# Create your views here.
class UserRegistrationApiView(UserCreateMixin,CreateAPIView):
    queryset=user.objects.all()
    serializer_class=UserInputSerializer
    permission_classes=[AllowAny]
    authentication_classes=[]


    def post(self, request, *args, **kwargs):
        return self.create(request)
    

# phonenumberverification
class PhoneNumberVerificationApiView(PhoneNumberVerificationMixin,CreateAPIView):
    serializer_class=PhoneNumberVerifyInputSerialzer
    permission_classes=[AllowAny]
    authentication_classes=[]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request)
    

class ResetPasswordApiView(CreateAPIView):
    serializer_class=ForgetPasswordInputSerializer
    permission_classes=[AllowAny,]
    authentication_classes=[]
    

class LoginApiView(TokenObtainPairView):
     def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            data={
                "message":error_handler(e),
                "status":"failed"     
            }
            raise AuthenticationFailed(data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def socialAuthentication(request,backend):
    token = request.data.get('access_token')
    try:
        user = request.backend.do_auth(token)
        if user:
            res=jwt_token(user)
            return Response(res,status=status.HTTP_200_OK,)
        return Response({
            'message':'user not found'
        },status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message':error_handler(e)},status=status.HTTP_200_OK,)



# class EmailConfirmationView(TemplateView):
#     template_name="accounts/email_Verification_Successful.html"

#     def get(self, request, *args, **kwargs):
#         uid=bytes_Converter(self.kwargs['uid'])
#         try:
#             instance=user.objects.get(id=uid)
#             instance.is_verified=True
#             instance.save()
#             context = {
#                 "name":instance.first_name
#             }
#         except Exception as e:
#                 data={
#                 "message":error_handler(e),
#                 "status":"failed"     
#             }
#                 raise AuthenticationFailed(data)
#         return self.render_to_response(context)
    
