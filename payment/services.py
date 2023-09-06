import hashlib
import hmac
from django.conf import settings
from typing import Dict
from .data_class import User
import requests
from rest_framework.exceptions import ValidationError
import json
from .transaction import Transactions
import codecs
BASE_URL="https://api.paystack.co/transaction"

class PaymentServices(object):

    def make_request(self,method,url,payload=None):
        authorization=settings.PAYSTACK_SECRET_KEY
        headers={
            "Authorization":f"Bearer {authorization}",
            "Content-Type": "application/json",
        }
        response=requests.request(method,url,data=json.dumps(payload),headers=headers)

        if response.status_code != 200:
            if response.text:
                raise ValidationError(response.text)
            else:
                raise ValidationError(
                    f"paystack failed with error code: {response.status_code}"
                )
        data_json_str = json.dumps(json.loads(response.text))
        # convert json str to json object
        result = json.loads(data_json_str)
        return result


 
    def initialize_transaction(self,payload:Dict,user:User):
        url=f"{BASE_URL}/initialize"
        body={
            "email":user.email,
            "amount":int(payload['amount'])*100,
            "metadata":{
                "user_id":str(user.id),
                "course_id":str(payload['course_id']),
                "full_name":f"{user.first_name} {user.last_name}"
            }
        }
        return self.make_request("POST",url,body)


    def verify_transaction(self,reference):
        url=f"{BASE_URL}/verify/{reference}"
        return self.make_request("GET",url)
    


        

class WebhookService(object):
    def __init__(self, request) -> None:
        self.request = request

    def webhook_handler(self):
        try:
            secret = settings.PAYSTACK_SECRET_KEY
        except Exception as e:  # If user hasn't declared variable
            raise ValidationError(e)
        req_body = self.request.body
        hash = hmac.new(codecs.encode(secret), req_body, digestmod=hashlib.sha512).hexdigest()
        if hash != self.request.headers["x-paystack-signature"]:
            raise ValidationError("MAC authentication failed")  
        else:
            body_unicode = req_body.decode('utf-8')
            body = json.loads(body_unicode)
            event = body['event']
            if event == "charge.success":
                paystack_service = Transactions()
                paystack_service.log_transaction(body["data"],body["data"]["customer"]["email"])

                customer_service = Transactions()
                context=customer_service.log_customer(body["data"])
        return context



