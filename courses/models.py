import os
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator,MaxValueValidator,MinValueValidator
import cv2
import datetime

# Create your models here.
class Category (models.Model):
    title=models.CharField(_("Title"),max_length=200,blank=False,null=False)

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    class LevelMode(models.TextChoices):
        Beginner="Beginner","Beginner"
        Intermidate="Intermidate","Intermidate"
        Advance="Advance","Advance"
    class StatusMode(models.TextChoices):
        Paid="Paid","Paid"
        Free="Free","Free"
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,db_index=True)
    title=models.CharField(_("Title"),max_length=300,blank=False,null=False)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    image=models.ImageField(upload_to='Course_img/%Y/%M',blank=False)
    price=models.DecimalField(_("Price"),max_digits=99999999,decimal_places=0,blank=True,null=True)
    discount=models.IntegerField(_("Discount",),null=True,blank=True)
    price_status=models.CharField(choices=StatusMode.choices,default=StatusMode.Free,max_length=15,blank=True,null=True)
    subscribers=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='enroll_courses')
    level=models.CharField(choices=LevelMode.choices,default=LevelMode.Beginner,max_length=15)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


    @property
    def discounted_price(self):
        if self.discount is not None:
            newprice=float(self.price)-(float(self.price)*(self.discount* 0.01))
            return newprice

       
    def save(self,) -> None:
        if self.price==None:
            self.price_status=Course.StatusMode.Free
        else:
            self.price_status=Course.StatusMode.Paid
        return super().save()


class SubCourse(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,db_index=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='subcourse')
    title=models.CharField(_("Title"),max_length=300,null=True,blank=True)


    def __str__(self) -> str:
        return self.title

class Lesson(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,db_index=True)
    subcourse=models.ForeignKey(SubCourse,on_delete=models.CASCADE,related_name='subcourse_lesson',null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    title=models.CharField(_("Title"),max_length=300,blank=False,null=False)
    is_locked=models.BooleanField(_('Is_Locked'),default=False)
    video = models.FileField(_('Video'),upload_to='videos_uploaded',null=False,validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    duration=models.DurationField(_("Duration"),blank=True,null=True)
    is_completed=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)


    def __str__(self) -> str:
        return self.title   
    

    def create_duration_handler(self):
        resovled_path=self.video.path.replace(os.sep,os.altsep)
        video = cv2.VideoCapture(resovled_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        seconds = frame_count // fps
        video_time = datetime.timedelta(seconds=seconds)
        self.duration=video_time
     
    def save(self) -> None:
        super().save(force_insert=False)
        self.create_duration_handler()
        return super().save(force_update=True)

class AboutCourse(models.Model):
     course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='about_course',null=True)
     description=models.TextField(_("Description"),blank=True,null=True)
     requirement=models.TextField(_("Requirement"),blank=True,null=True)


     def __str__(self) -> str:
         return self.course.title


class Review(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False,db_index=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='reviews')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="user_review")
    review=models.TextField()
    rating=models.IntegerField(_("Rating"),validators=[MaxValueValidator(limit_value=5),MinValueValidator(limit_value=0)])
    date_created=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=["-date_created"]


    def __str__(self) -> str:
        return self.course.title
    


     
