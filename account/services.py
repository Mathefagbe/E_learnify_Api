import string,datetime
from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import EmailVerification
from django.contrib.auth import get_user_model
from utils.error_handler import error_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()


def verify_account(self,request):
        '''
        User verify first before creating an account and becoming a user
        
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp=serializer.validated_data.get('otp_code',None)
        if not User.objects.filter(email__iexact=serializer.validated_data['email']).exists():
                if otp is None and not EmailVerification.objects.filter(email__iexact=serializer.validated_data['email']).exists() :
                    generated_otp=get_random_string(6,allowed_chars=string.digits)
                    serializer.save(otp=generated_otp)
                    headers = self.get_success_headers(serializer.data)
                    return Response(data={
                                'message':"success",
                                'data':serializer.data,
                                'status':"success"
                            },status=status.HTTP_201_CREATED,headers=headers)
                
                elif otp is None and EmailVerification.objects.filter(email__iexact=serializer.validated_data['email']).exists():
                    instance=EmailVerification.objects.get(email__iexact=serializer.validated_data['email'])
                    serialized_instance=self.get_serializer(instance=instance, data=request.data)
                    serialized_instance.is_valid(raise_exception=True)
                    serialized_instance.save()
                    headers = self.get_success_headers(serialized_instance.data)
                    return Response(data={
                                'message':"success",
                                'data':serialized_instance.data,
                                'status':"success"
                            },status=status.HTTP_201_CREATED,headers=headers)
                else:
                    try:
                        instance=EmailVerification.objects.get(email__iexact=serializer.validated_data['email'],otp_code=otp)
                        if instance.date_generated + datetime.timedelta(seconds=60)> datetime.datetime.now(datetime.timezone.utc):
                            serialized_instance=self.get_serializer(instance=instance, data=request.data)
                            serialized_instance.is_valid(raise_exception=True)
                            serialized_instance.save(verify=True)
                            headers = self.get_success_headers(serialized_instance.data)
                            return Response(data={
                                'message':"success",
                                'data':serialized_instance.data,
                                'status':"success"
                            },status=status.HTTP_201_CREATED,headers=headers)
                        else:
                            return Response(data={
                                'message':error_handler("Verification Link Has Expired"),
                                'status':"Failed"
                            },status=status.HTTP_205_RESET_CONTENT)
                    except Exception as e:
                        return Response(data={
                                'message':error_handler("You entered wrong OTP code,please check it again"),
                                'status':"Failed"
                            },status=status.HTTP_404_NOT_FOUND)
        else:
             return Response(data={
                                'message':error_handler("email has been linked to an account"),
                                'status':"Failed"
                            },status=status.HTTP_409_CONFLICT)
                        
                



def forgetpassword_email_verification(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp=serializer.validated_data.get('otp',None)
        '''
        For forgetpassword verification the email has to be registered
        has a user before forgetpassword verification can send otp
        '''
        if User.objects.filter(email__iexact=serializer.validated_data['email']).exists(): 
                if otp is None and EmailVerification.objects.filter(email__iexact=serializer.validated_data['email']).exists():
                    instance=EmailVerification.objects.get(email__iexact=serializer.validated_data['email'])
                    serialized_instance=self.get_serializer(instance=instance, data=request.data)
                    serialized_instance.is_valid(raise_exception=True)
                    serialized_instance.save()
                    headers = self.get_success_headers(serialized_instance.data)
                    return Response(data={
                                'message':"success",
                                'data':serialized_instance.data,
                                'status':"success"
                            },status=status.HTTP_201_CREATED,headers=headers)
                else:
                    try:
                        instance=EmailVerification.objects.get(email__iexact=serializer.validated_data['email'],otp_code=otp)
                        if instance.date_generated + datetime.timedelta(seconds=60)> datetime.datetime.now(datetime.timezone.utc):
                            serialized_instance=self.get_serializer(instance=instance, data=request.data)
                            serialized_instance.is_valid(raise_exception=True)
                            serialized_instance.save()
                            headers = self.get_success_headers(serialized_instance.data)
                            return Response(data={
                                'message':"success",
                                'data':serialized_instance.data,
                                'status':"success"
                            },status=status.HTTP_201_CREATED,headers=headers)
                        else:
                            return Response(data={
                                'message':error_handler("Verification Link Has Expired"),
                                'status':"Failed"
                            },status=status.HTTP_205_RESET_CONTENT)
                    except Exception as e:
                        return Response(data={
                                'message':error_handler("You entered wrong OTP code,please check it again"),
                                'status':"Failed"
                            },status=status.HTTP_404_NOT_FOUND)
        else:
             return Response(data={
                                'message':error_handler("you have entered a wrong email"),
                                'status':"Failed"
                            },status=status.HTTP_404_NOT_FOUND)
                        
                
@staticmethod
def check_verification(user):
    try:
          verify_user=EmailVerification.objects.get(email__iexact=user.email)
          if not verify_user.verify:
               raise serializers.ValidationError("you haven't verified your email")
    except Exception as e:
        raise serializers.ValidationError("you haven't verified your email")



@staticmethod
def check_isactive(user):
     if not User.is_active:
          raise serializers.ValidationError('You have been disabled')
     

    

@staticmethod
def social_jwt_token(user):
    data={}
    refresh=RefreshToken.for_user(user)
    # refresh=TokenObtainPairSerializer.get_token(user)     
    data["refresh"] = str(refresh)
    data["access"] = str(refresh.access_token)
    return data