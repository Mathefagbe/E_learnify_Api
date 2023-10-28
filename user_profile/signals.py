from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile,UserProfile


#this function will only be triggered when a new instance of user is created
# @receiver will listen for changes in the user after user is created.

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender,instance,created,**kwargs):
    if created:
        if instance.is_instrutor:
            instructor_profile=InstructorProfile()
            instructor_profile.instructor=instance
            instructor_profile.save()
            return instructor_profile
        else:
            user_profile=UserProfile()
            user_profile.user=instance
            user_profile.save()
            return user_profile