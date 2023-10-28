from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    image=models.ImageField(upload_to="Profile_Images")
    about=models.TextField(blank=True,null=True)
    # imageurl=models.URLField(blank=True,null=True)
    github_link=models.CharField(max_length=200,blank=True,null=True)
    facebook_link=models.CharField(max_length=200,blank=True,null=True)
    linkedin_link=models.CharField(max_length=200,blank=True,null=True)
    
    class Meta:
        abstract=True


class UserProfile(Profile):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_profile')
    
    def __str__(self) -> str:
        return self.user.email

class InstructorProfile(Profile):
    instructor=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='instructor_profile',null=True)
    headline=models.CharField(max_length=200,blank=True,null=True)
    website=models.CharField(max_length=300,blank=True,null=True)


    def __str__(self) -> str:
        return self.instructor.email

