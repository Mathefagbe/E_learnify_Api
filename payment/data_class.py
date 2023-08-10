from dataclasses import dataclass
from datetime import datetime
from django.contrib.auth import get_user_model

@dataclass
class Authorization:
    bin:str
    last4:str
    exp_month:str
    exp_year:str
    account_name:str
    signature:str

@dataclass
class User:
    id:str
    first_name=str
    last_name=str
    email:str
    customer_code:str

@dataclass
class Metadata:
        first_name=str
        last_name=str


@dataclass
class PaymentDataInfo:
    id:str
    status:str
    reference:str
    amount:int
    gateway_response:str
    transaction_date:str(datetime)
    paid_at:str(datetime)
    fee:str
    receipt_number:str
    channel:str
    customer:User
    authorization:Authorization


@dataclass
class PaymentPayloadInfo:
    data:PaymentDataInfo
  