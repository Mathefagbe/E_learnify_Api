from django.urls import path as url
from .views import (FcmTokenSaver)


urlpatterns = [
    url('token/',FcmTokenSaver.as_view(),name='token'),
    
]