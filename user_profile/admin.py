from django.contrib import admin
from .models import UserProfile,InstructorProfile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,ProfileAdmin)
admin.site.register(InstructorProfile,ProfileAdmin)