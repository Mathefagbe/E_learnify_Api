from rest_framework import serializers
from .models import Course
from account.serializers import UserOutputSerializer
from .models import Lesson,Category,Review,SubCourse,AboutCourse
from django.utils.timesince import timesince
from utils.base_serializers import BaseCourseSerializers
import datetime


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
    discount_price=serializers.DecimalField(source='discounted_price',max_digits=99999999,decimal_places=0)
    class Meta:
        model=Course
        fields=['id','title','total_duration','total_lesson',
                'price','discount_price','average_rating',]


class CourseDetailOutputSerializer(BaseCourseSerializers):
    category=CategorySerializer(read_only=True)
    discount_price=serializers.DecimalField(source='discounted_price',max_digits=99999999,decimal_places=0)
    author=None
    progress=None
    total_duration=None
    total_lesson = None
    class Meta:
        model=Course
        exclude=['subscribers','author','discount','date_created','date_updated']


class CourseInputSerializer(serializers.ModelSerializer):

    class Meta:
        model=Course
        fields=['title','category','image',"price",'discount','author']
        

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


class AboutCourseSerializer(serializers.ModelSerializer):
    date_created=serializers.DateTimeField(source='course.date_created')
    total_lesson=serializers.SerializerMethodField()
    total_duration=serializers.SerializerMethodField()
    author=UserOutputSerializer(read_only=True,source='course.author')
    level=serializers.CharField(read_only=True,source='course.level')
    class Meta:
        model=AboutCourse
        fields=['author','description','requirement','date_created',
                'total_lesson','total_duration','level']


    def get_total_lesson(self,obj):
       return f"{obj.course.lessons.count()} Lessons"
    
    def get_total_duration(self,obj):
        duration_list=[]
        for course_length in obj.course.lessons.all():
                duration_list.append(course_length.duration.seconds)
        total_seconds=sum(duration_list)
        hour,minute,second=str(datetime.timedelta(seconds=total_seconds)).split(":")
        return f"{int(minute)} mins" if int(hour)==0 else f"{int(hour)} hrs {int(minute)} mins"