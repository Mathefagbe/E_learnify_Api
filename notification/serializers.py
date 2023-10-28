from rest_framework import serializers
from fcm_django.models import FCMDevice
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    owner=serializers.CharField(source="owner.email")
    class Meta:
        model=Notification
        exclude=['id']

