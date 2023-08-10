import uuid
from django.db import models
from django.conf import settings
from courses.models import Course

class PayStackCustomer(models.Model):
    """
    for charging a customer's card again using authorization code
    for transfers too
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # authorization creds for recurring charges
    email = models.CharField(blank=True, null=True, max_length=100)
    authorization_code = models.CharField(blank=True, null=True, max_length=100)
    card_type = models.CharField(blank=True, null=True, max_length=10)
    last4 = models.CharField(blank=True, null=True, max_length=4)
    exp_month = models.CharField(blank=True, null=True, max_length=10)
    exp_year = models.CharField(blank=True, null=True, max_length=10)
    bin = models.CharField(blank=True, null=True, max_length=10)
    bank = models.CharField(blank=True, null=True, max_length=100)
    account_name = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return f"{self.user} paymentinfo"

class TransactionLog(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4,primary_key=True)
    course=models.ForeignKey(Course,on_delete=models.SET_NULL, null=True,editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(max_length=19)
    currency = models.CharField(max_length=5)
    txRef = models.CharField(max_length=100, null=True, blank=True)
    payment_date_time = models.DateTimeField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    gateway_response=models.CharField(max_length=50, null=True, blank=True)
    transactionComplete = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} - checkout_id: {self.txRef}"