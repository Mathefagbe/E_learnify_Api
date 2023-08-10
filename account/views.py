from rest_framework.generics import CreateAPIView
from account.services import (forgetpassword_email_verification,
                              verify_account,social_jwt_token)
from.serializers import (UserInputSerializer,UserEmailVerifyInputSerialzer,
                         ForgetPasswordEmailVerifyInputSerialzer,ForgetPasswordInputSerializer,
                         TokenObtainPairSerializer)
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework import status
from django.contrib.auth import get_user_model
from utils.error_handler import error_handler
from rest_framework_simplejwt.views import (TokenObtainPairView)
from rest_framework.exceptions import AuthenticationFailed,ValidationError
from social_django.utils import psa
from rest_framework.decorators import api_view,permission_classes


user=get_user_model()
# Create your views here.
class UserRegistrationApiView(CreateAPIView):
    queryset=user.objects.all()
    serializer_class=UserInputSerializer
    permission_classes=[AllowAny]
    authentication_classes=[]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login_serializer=TokenObtainPairSerializer(data=request.data)
            login_serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)    
        except Exception as e:
            data={
                "message":error_handler(e),
                "status":"failed"     
            }
            raise ValidationError(data)
        return Response(headers=headers, data={
            "message":"success",
            'data':serializer.data,
            'token':login_serializer.validated_data,
            "status":"success"
        },status=status.HTTP_201_CREATED)


class EmailVerificationApiView(CreateAPIView):
    serializer_class=UserEmailVerifyInputSerialzer
    permission_classes=[AllowAny,]
    authentication_classes=[]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return verify_account(self,request)
    

class ForgetPasswordEmailVerificationApiView(CreateAPIView):
    serializer_class=ForgetPasswordEmailVerifyInputSerialzer
    permission_classes=[AllowAny,]
    authentication_classes=[]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return forgetpassword_email_verification(self,request)
    

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
            res=social_jwt_token(user)
            return Response(res,status=status.HTTP_200_OK,)
        return Response({
            'message':'user not found'
        },status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message':error_handler(e)},status=status.HTTP_200_OK,)
