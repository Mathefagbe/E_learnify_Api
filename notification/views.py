from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotificationSerializer
from .models import Notification
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet,FCMDeviceCreateOnlyViewSet,FCMDeviceViewSet


class FCMDeviceNotifiyCreateOnlyViewSet(FCMDeviceAuthorizedViewSet):
    authentication_classes=[BasicAuthentication]


class NotificationApiView(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]


    def get(self,request,*args,**kwargs):
            obj=Notification.objects.select_related('owner').\
                filter(owner=self.request.user)
            self.check_object_permissions(self.request, obj)
            serializer=NotificationSerializer(obj,many=True)
            return Response(serializer.data)




