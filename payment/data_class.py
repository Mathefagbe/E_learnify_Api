from dataclasses import dataclass
from datetime import datetime
from django.contrib.auth import get_user_model


@dataclass
class User:
    id:str
    first_name=str
    last_name=str
    email:str
    customer_code:str




