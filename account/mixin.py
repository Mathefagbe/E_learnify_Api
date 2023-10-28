from rest_framework.response import Response
from rest_framework import status
from utils.error_handler import error_handler
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from utils.error_handler import error_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import PhoneNumberVerification
import string,datetime
from django.utils.crypto import get_random_string



User=get_user_model()

class UserCreateMixin:

    def create(self,request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return self.perform_create(serializer)
        except Exception as e:
            self.exceptions(e)

    def exceptions(self,error):
        data={"message":error_handler(error),
                "status":"failed"}
        raise ValidationError(data)
    
        
    def perform_create(self,serializer):
        serializer.save()
        headers = self.get_success_headers(serializer.data)  
        return Response(headers=headers, data={"message":"success",
            'data':serializer.data,
            "status":"success"},
            status=status.HTTP_201_CREATED)
           

class PhoneNumberVerificationMixin:

    def create(self,request,*args,**kwargs):
        phone_no=request.data['phone_no']
        otp=request.data.get('otp_code',None)
        try:
            if User.objects.filter(phone_no=phone_no).exists():
                instance=PhoneNumberVerification.objects.filter(phone_no=phone_no).first()
                # can_exist=PhoneNumberVerification.objects.filter(phone_no=phone_no).exists()
                if instance and otp is None:
                    instance_serializer = self.get_serializer(instance=instance,data=request.data)
                    instance_serializer.is_valid(raise_exception=True)
                    return self.perform_update(instance_serializer)
                elif otp is None and not instance:
                    serializer=self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    return self.perform_create(serializer)
                else:
                    try:
                        user_data=PhoneNumberVerification.objects.get(phone_no=phone_no,otp_code=otp)
                        return self.can_do_verification(user_data,phone_no)
                    except Exception as e:
                        return Response(data={
                        'message':error_handler("You entered wrong OTP code,please check it again"),
                        'status':"Failed"
                    },status=status.HTTP_404_NOT_FOUND)
            return Response(data={
                        'message':error_handler("you have entered a wrong phone_no"),
                        'status':"Failed"
                    },status=status.HTTP_404_NOT_FOUND)
                     
        except Exception as e:
            data={
                "message":error_handler(e),
                "status":"failed"     
            }
            raise ValidationError(data)

    def perform_create(self,serializer):
        generated_otp=get_random_string(6,allowed_chars=string.digits)
        serializer.save(otp_code=generated_otp)
        self.send_otp(serializer.data['otp_code'])
        headers = self.get_success_headers(serializer.data)
        return Response(data={
                'message':"success",
                'data':serializer.data,
                'status':"success"
        },status=status.HTTP_201_CREATED,headers=headers)
    
    def perform_update(self,serializer):
        otp=get_random_string(6,allowed_chars=string.digits)
        serializer.save(otp_code=otp)
        self.send_otp(serializer.data['otp_code'])
        headers = self.get_success_headers(serializer.data)
        return Response(data={
                'message':"success",
                'data':serializer.data,
                'status':"success"
        },status=status.HTTP_201_CREATED,headers=headers)

    def send_otp(self,otp):
        print(f"otp has been sent to your phone {otp}")
    def check_verification(self,user):
        if not user.is_verified:
            return self.not_verified(user)
        else:
            return Response(data={
                'message':"success",
                # "data":jwt_token(user),
                'status':"success"
            },status=status.HTTP_200_OK)                     

    def not_verified(self,user):
            user.is_verified=True
            user.save()
            return Response(data={
                    'message':"user not verified",
                    # "data":jwt_token(user),
                    'status':"success"
                },status=status.HTTP_200_OK)
    
    def can_do_verification(self,user_data,phone_no):
        if user_data.date_generated + datetime.timedelta(seconds=60) > datetime.datetime.now(datetime.timezone.utc):
            user_detail=User.objects.get(phone_no=phone_no)
            return self.check_verification(user_detail)
        else:
            return Response(data={
                    'message':error_handler("Verification Link Has Expired"),
                    'status':"Failed"
            },status=status.HTTP_205_RESET_CONTENT)
