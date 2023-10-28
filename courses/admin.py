from django.contrib import admin
from .models import Category,Course,Lesson,Review,SubCourse,AboutCourse,Requirement
from django.utils.translation import gettext_lazy as _



admin.site.register(Category)
admin.site.register(AboutCourse)
admin.site.register(Review)
admin.site.register(Requirement)
class CustomLesson(admin.ModelAdmin):
    model=Lesson
    list_display=['course',"title",'subcourse']

    fieldsets = (
        (None, {"fields": ('course','title','subcourse',
                           'is_locked','is_completed','video',)}),)
admin.site.register(Lesson,CustomLesson)

class CustomCourse(admin.ModelAdmin):
    model=Course
    list_display=['author',"title",'category','level','price_status']
    fieldsets = (
        (None, {"fields": ('title','author','category','image',
                           'price','discount','level','subscribers')}),
                        #    'subscribers'
    )
admin.site.register(Course,CustomCourse)

class CustomSubCourse(admin.ModelAdmin):
    model=Course
    list_display=["title",'course']
    fieldsets = (
        (None, {"fields": ("title",'course')}),
                        #    'subscribers'
    )
admin.site.register(SubCourse,CustomSubCourse)