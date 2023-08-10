from django.contrib import admin
from .models import PayStackCustomer,TransactionLog

# Register your models here.
class PaystackAdmin(admin.ModelAdmin):
    model=PayStackCustomer
    list_display=["user","email","authorization_code","card_type",
                  "last4","exp_month",'exp_year','bin',
                  ]
    fieldsets = (
        (None, {"fields": ("user","email","authorization_code","card_type",
                  "last4","exp_month",'exp_year','bin',
                  'bank',"account_name")}),                 
    )
admin.site.register(PayStackCustomer,PaystackAdmin)

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