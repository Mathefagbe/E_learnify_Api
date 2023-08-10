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
                 'category','date_created','date_updated','author','lessons','reviews','subscribers']
        
    def get_total_lesson(self,obj):
       return f"{obj.lessons.count()} Lessons"
    
    def get_total_duration(self,obj):
        # duration_list=[]
        # for course_length in obj.lessons.all():
        #         duration_list.append(course_length.duration.seconds)
        total_seconds=sum([course_length.duration.seconds for course_length in obj.lessons.all()])
        hour,minute,second=str(datetime.timedelta(seconds=total_seconds)).split(":")
        return f"{int(minute)} mins" if int(hour)==0 else f"{int(hour)} hrs {int(minute)} mins"
    
    
    def get_progress(self,obj):
        try:
            completed_course=obj.lessons.filter(is_completed=self.context['user']).count()
            total_lessons=obj.lessons.count()
            percentage=(completed_course/total_lessons)*100
            return round(percentage)
        except ZeroDivisionError as e:
            return 0
    

    def get_average_rating(self,obj):
        try:
            rate=sum([rate.rating for rate in obj.reviews.all()])
            length=obj.reviews.count()
            average=rate/length
            return round(average,ndigits=2)
        except ZeroDivisionError as e:
            return 0
     
    
    