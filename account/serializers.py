from rest_framework import serializers
from account.services import check_verification,check_isactive
from .models import CustomUser,PhoneNumberVerification
from django.utils.crypto import get_random_string
import string
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


# User=get_user_model()
class UserInputSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True,write_only=True)

    class Meta:
        model=CustomUser
        fields=['id','email','first_name','last_name','phone_no'
                "is_verified","is_staff",'password','confirm_password']
        extra_kwargs={
            'password':{"write_only":True},
            "is_verified":{"read_only":True },
            "is_staff":{"read_only":True },
            "id":{"read_only":True}
            }
        
    def validate(self, attrs):
        password=attrs.get('password',None)
        confirm_password=attrs.get('confirm_password',None)
        email=attrs.get('email',None)
        if password!=confirm_password:
            raise serializers.ValidationError({'detail':"Password doesn't match"})
        elif CustomUser.objects.filter(email__iexact=email):
            raise serializers.ValidationError({'detail':'Email Already Exist'})
        return attrs
      
    def create(self, validated_data):
        user=CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.confirm_password=user.password
        user.save()
        return user


class UserOutputSerializer(serializers.ModelSerializer):
    full_name=serializers.CharField(source='get_full_name')
    class Meta:
        model=CustomUser
        fields=['id','full_name','email',]

class PhoneNumberVerifyInputSerialzer(serializers.ModelSerializer):
    class Meta:
        model=PhoneNumberVerification
        fields=['phone_no','otp_code']
        extra_kwargs={
            "date_created":{"read_only":True} }

    def validate(self, attrs):
        phone_no=attrs.get('phone_no',None)
        if phone_no is None:
            raise serializers.ValidationError({"detail":"please enter a valid phone Number"})
        return attrs

    def create(self, validated_data):
     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.phone_no=validated_data.get('phone_no',instance.phone_no)
    #     generated_otp=get_random_string(6,allowed_chars=string.digits)
    #     instance.otp_code=validated_data.get('otp_code',generated_otp)
    #     instance.save()
    #     return instance


class ForgetPasswordInputSerializer(serializers.Serializer):
    phone_no=serializers.CharField(required=True,max_length=12)
    password=serializers.CharField(required=True, write_only=True)
    confirm_password=serializers.CharField(required=True,write_only=True)

    def validate(self, attrs):
        if attrs['password']==attrs['confirm_password']:
            return attrs
        raise serializers.ValidationError({"password doesn't match"})


    def create(self, validated_data):
        try:   
            new_password=validated_data.get('password')
            user=CustomUser.objects.get(phone_no=validated_data['phone_no'])
            user.set_password(new_password)
            user.confirm_password=user.password
            user.save()
        except Exception as e:
            raise serializers.ValidationError(e)
        return user


class TokenObtainPairSerializer(TokenObtainSerializer):
    default_error_messages = {
        "no_active_account": _("login provided credentials does not exist")
    }
    token_class = RefreshToken
    def validate(self, attrs):
        data = super().validate(attrs)
       # check if the user is still is active or not
        check_isactive(self.user)
        # check if the user is verified before he can successfully login in
        check_verification(self.user)     
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data



    