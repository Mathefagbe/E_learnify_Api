from rest_framework import serializers
from .models import Course
from account.serializers import UserOutputSerializer
from .models import Lesson,Category,Review,SubCourse,AboutCourse,Requirement
from django.utils.timesince import timesince
from utils.base_serializers import BaseCourseSerializers
from user_profile.serializers import InstructorSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class LessonOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        exclude=['is_completed','subcourse','course']
        extra_kwargs={
            'duration':{
                "read_only":True
            }
        }

class SubCourseOutputSerializer(serializers.ModelSerializer):
    subcourse_lesson=LessonOutputSerializer(many=True)
    class Meta:
        model=SubCourse
        fields=['title','subcourse_lesson']


class CourseOutputSerializer(BaseCourseSerializers):
    discount_price=serializers.DecimalField(source='discounted_price',max_digits=10,decimal_places=0)
    class Meta:
        model=Course
        fields=['id','title','total_duration','total_lesson',
                'price','discount_price','average_rating',]
        
        read_only=fields


class CourseDetailOutputSerializer(BaseCourseSerializers):
    # category=CategorySerializer(read_only=True)
    category=serializers.CharField(source='category.title')
    discount_price=serializers.DecimalField(source='discounted_price',max_digits=10,decimal_places=0)
    author=None
    progress=None
    total_duration=None
    total_lesson = None
    class Meta:
        model=Course
        exclude=['subscribers','author','discount','date_created','date_updated']






class ReviewSerializer(serializers.ModelSerializer):
    user=UserOutputSerializer(read_only=True)
    time_since=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Review
        fields=['id','review','rating','user','time_since']
        extra_kwargs={  
            'id':{
                'read_only':True
            }
        }
    def get_time_since(self,obj):
       timeAgo=timesince(obj.date_created)
       formatedTime=timeAgo.split(',')[0]
       return  f"{formatedTime} ago"
    

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Requirement
        exclude=["id",'about_course']

class AboutCourseSerializer(serializers.ModelSerializer):
    date_created=serializers.DateTimeField(source='course.date_created')
    total_lesson=serializers.SerializerMethodField()
    total_duration=serializers.SerializerMethodField()
    author=InstructorSerializer(read_only=True,source='course.author.instructor_profile')
    level=serializers.CharField(read_only=True,source='course.level')
    requirements=serializers.StringRelatedField(many=True)

    class Meta:
        model=AboutCourse
        fields=['author','description','date_created',
                'total_lesson','total_duration','level','requirements']


    def get_total_lesson(self,obj):
       return f"{obj.course.lessons.count()} Lessons"
    
    
    def get_total_duration(self,obj):
        if obj.total_duration is not None:
            hour,minute,second=str(obj.total_duration).split(":")
            return f"{int(minute)} mins" if int(hour)==0 else f"{int(hour)} hrs {int(minute)} mins"