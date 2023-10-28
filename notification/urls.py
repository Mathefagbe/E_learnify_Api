from django.urls import path as url
from .views import (FCMDeviceNotifiyCreateOnlyViewSet,NotificationApiView)
from fcm_django.api.rest_framework import FCMDeviceCreateOnlyViewSet,FCMDeviceAuthorizedViewSet


urlpatterns = [
    url("device/",FCMDeviceNotifiyCreateOnlyViewSet.as_view({'post':'create'}),name="create_fcm_device"),
    url('notification/',NotificationApiView.as_view(),name="notification")
]