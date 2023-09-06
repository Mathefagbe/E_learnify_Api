from rest_framework import serializers
from fcm_django.models import FCMDevice

class TokenSerializer(serializers.ModelSerializer):
    token=serializers.CharField(source="registration_id")

    
    class Meta:
        model=FCMDevice
        fields=["token"]


    def update(self, instance, validated_data):
        token=validated_data.get('token',None)
        instance.token=token
        instance.save()
        return instance