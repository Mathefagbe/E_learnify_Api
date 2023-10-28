from django.contrib import admin
from .models import TransactionLog

# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    model=TransactionLog
    list_display=["user","course","currency","amount","txRef",
                  "status","gateway_response",
                  'payment_date_time']
    fieldsets = (
        (None, {"fields": ("user","currency","amount","txRef",
                  "status","gateway_response",
                  'payment_date_time',"transactionComplete")}),                 
    )
admin.site.register(TransactionLog,TransactionAdmin)