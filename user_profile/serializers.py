from rest_framework import serializers
from .models import Profile


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','user','title','about','image','github_link','facebook_link','linkedin_link']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','user','about','image','github_link','facebook_link','linkedin_link']