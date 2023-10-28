from rest_framework import serializers
from courses.models import Course
import datetime
from account.serializers import UserOutputSerializer


class BaseCourseSerializers(serializers.ModelSerializer):
    total_lesson=serializers.SerializerMethodField()
    total_duration=serializers.SerializerMethodField()
    author=UserOutputSerializer(read_only=True)
    progress=serializers.SerializerMethodField(read_only=True)
    average_rating=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Course
        exclude=['status',
                 'category','date_created','date_updated',
                 'author','lessons','reviews','subscribers']
        
    def get_total_lesson(self,obj):
       return f"{obj.lessons.count()} Lessons"
    
    def get_total_duration(self,obj):
        if obj.total_lesson is not None:
            hour,minute,second=str(obj.total_lesson).split(":")
            return f"{int(minute)} mins" if int(hour)==0 else f"{int(hour)} hrs {int(minute)} mins"
    
    
    def get_progress(self,obj):
        try:
            completed_course=obj.completed_lesson
            total_lessons=obj.total_lesson
            percentage=(completed_course/total_lessons)*100
            return round(percentage)
        except ZeroDivisionError as e:
            return 0
    

    def get_average_rating(self,obj):
        try:
            length=obj.avg_rating
            return round(length,ndigits=2) if type(length) == 'float' else length
        except ZeroDivisionError as e:
            return 0
     
    
    