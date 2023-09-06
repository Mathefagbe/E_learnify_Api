from rest_framework.views import APIView
from fcm_django.models import FCMDevice
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class FcmTokenSaver(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token=self.request.data.get('token',None)
        if  FCMDevice.objects.filter(user=self.request.user).exists():
            instance=FCMDevice.objects.get(user=self.request.user)
            instance.registration_id=token
            instance.save()
        else:
            device=FCMDevice()
            device.registration_id=token
            device.user=self.request.user
            device.save()
        context={
            "status":"success",
            "message":"ok",
            "data":"created"
        }
        return Response(context,status=status.HTTP_201_CREATED)
