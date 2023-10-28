from rest_framework import serializers
from .models import InstructorProfile,UserProfile



class InstructorSerializer(serializers.ModelSerializer):
    instructor=serializers.CharField(read_only=True,source='instructor.get_full_name')
    email=serializers.CharField(read_only=True,source='instructor.email')
    class Meta:
        model=InstructorProfile
        fields=['id','instructor','email','headline','about','image',
                'github_link','facebook_link','linkedin_link']


class UserSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True,source='user.get_full_name')
    email=serializers.CharField(read_only=True,source='user.email')
    class Meta:
        model=UserProfile
        fields=['user','email','about','image',
                'github_link','facebook_link','linkedin_link']
  