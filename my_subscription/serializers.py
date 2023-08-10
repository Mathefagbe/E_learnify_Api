from rest_framework import serializers
from account.serializers import UserOutputSerializer
from courses.models import Course
# from .models import MyLearning
from courses.models import Lesson,SubCourse
from courses.serializers import CategorySerializer
from utils.base_serializers import BaseCourseSerializers
from django.contrib.auth import get_user_model


User=get_user_model()

class EnrolledLessonOutputSerializer(serializers.ModelSerializer):
    is_locked=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Lesson
        exclude=['is_completed','subcourse','course']
        extra_kwargs={
            'duration':{
                "read_only":True
            }
        }
    def get_is_locked(self,obj):
        obj.is_locked=False
        return obj.is_locked
         

class AuthorOnlyCourseSerializer(BaseCourseSerializers):
    class Meta:
        model=Course
        fields=['author','title']
        

class EnrollSubCourseOutputSerializer(serializers.ModelSerializer):
    subcourse_lesson=EnrolledLessonOutputSerializer(many=True)
    class Meta:
        model=SubCourse
        fields=['title','subcourse_lesson',]




class EnrolledCourseDetailOutputSerializer(BaseCourseSerializers):
    category=CategorySerializer(read_only=True)
    progress=None
    total_duration=None
    total_lesson = None
    class Meta:
        model=Course
        exclude=['price','discount','subscribers','date_updated',]


class EnrolledCourseOutputSerializer(BaseCourseSerializers):
    
    class Meta:
        model=Course
        fields=['id','title','image','progress']


class MyLearningSerializer(serializers.ModelSerializer):
    enroll_courses=EnrolledCourseOutputSerializer(many=True)
    class Meta:
        model=User
        fields=['enroll_courses']
        
        