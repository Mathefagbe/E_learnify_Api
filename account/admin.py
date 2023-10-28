from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,PhoneNumberVerification
from django.utils.translation import gettext_lazy as _

# Register your models here.
class CustomAdmin(UserAdmin):
    model=CustomUser
    list_display=['email','first_name','last_name',"is_staff",'is_verified']
    ordering=[]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('email','first_name','last_name',"password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ( "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email",'phone_no')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    'is_verified',
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
admin.site.register(CustomUser,CustomAdmin)

class EmailVerifyAdmin(admin.ModelAdmin):
    model=PhoneNumberVerification
    list_display=["phone_no",'otp_code']
    fieldsets = (
        (None, {"fields": ("phone_no",'otp_code')}),
    )
admin.site.register(PhoneNumberVerification,EmailVerifyAdmin)
