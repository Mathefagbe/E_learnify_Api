from .models import TransactionLog,PayStackCustomer
from courses.models import Course
from rest_framework.exceptions import NotFound
from utils.error_handler import error_handler
from django.contrib.auth import get_user_model
from courses.models import Course

User=get_user_model()

class Transactions(object):
    def _get_user_by_email(self,email:str):
      user=User.objects.get(email=email)
      return user


    def _create_transaction_object(self, transaction_data,user):
        course_id=transaction_data['metadata']['course_id']
        course=Course.objects.get(id=course_id)
        TransactionLog.objects.create(
            user=user,
            amount=round(transaction_data["amount"]/100),
            currency=transaction_data["currency"],
            txRef=transaction_data["reference"],
            payment_date_time=transaction_data["paid_at"],
            status=transaction_data["status"],
            course=course,
            transactionComplete=True,
            gateway_response=transaction_data['gateway_response']
        )
        # course_id=transaction_data['metadata']['course_id']
        return self.enroll_to_course(course_id,user)

    def _create_customer_object(self,customer_data, authorization_data):
        user=self._get_user_by_email(email=customer_data["email"])
        defaults = {
            "user": user,
            "email": customer_data["email"],
            "authorization_code": authorization_data["authorization_code"],
            "card_type": authorization_data["card_type"],
            "last4": authorization_data["last4"],
            "exp_month": authorization_data["exp_month"],
            "exp_year": authorization_data["exp_year"],
            "bin": authorization_data["bin"],
            "bank": authorization_data["bank"],
            "account_name": authorization_data["account_name"],
        }

        PayStackCustomer.objects.update_or_create(**defaults, defaults=defaults)

    def log_customer(self,customer_data) -> None:
        customer_detail = customer_data["customer"]
        authorization_data = customer_data["authorization"]
        self._create_customer_object(customer_detail,authorization_data)


    def log_transaction(self, transaction_data,email):
       user=self._get_user_by_email(email=email)
       return self._create_transaction_object(transaction_data,user)

    
    @staticmethod
    def enroll_to_course(course_id,user):
        try:
            get_course=Course.objects.get(id=course_id)
            get_course.subscribers.add(user)
            context={
                'status':f'congratulations You Have successfully Enrolled For {get_course.title}'
            }
        except Exception as e:
            raise NotFound(error_handler(e))
        return context