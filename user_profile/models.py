from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="Profile_Images")
    title=models.CharField(max_length=200,blank=True,null=True)
    about=models.TextField(blank=True,null=True)
    github_link=models.CharField(max_length=200,blank=True,null=True)
    facebook_link=models.CharField(max_length=200,blank=True,null=True)
    linkedin_link=models.CharField(max_length=200,blank=True,null=True)

    def __str__(self) -> str:
        return self.user.first_name