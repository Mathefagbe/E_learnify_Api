from django.db import models
from django.conf import settings


class Notification(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    title=models.CharField(max_length=200,null=True,blank=True)
    message=models.TextField(null=True,blank=True)
    date_create=models.DateTimeField(auto_now=True)



