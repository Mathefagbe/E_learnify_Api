import requests
from dataclasses import dataclass
from dacite import from_dict


@dataclass
class User:
    id: str
    full_name: str
    email: str


@dataclass
class Comment:
    id: str
    review: str
    rating: int
    user: User
    time_since: str



endpoint="http://127.0.0.1:8000/api/course/aefaf352-1bc6-400f-990f-c7dde70b1fda/review/create/"
endpoint_2="http://127.0.0.1:8000/api/course/aefaf352-1bc6-400f-990f-c7dde70b1fda/"
headers={
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxMzE4NDA5LCJpYXQiOjE2OTEyNTA3MTYsImp0aSI6ImY1YmQwZWNmNmQzMDQ5NjI5MmFlZGYzZmE2NDc2YWVjIiwidXNlcl9pZCI6ImI0YmU1YzRiLTk3YzItNDk0MC04N2ViLTE3NDM3OTQ5OTA0ZiJ9.Vr0yMBYFCIz16LwdnPVZlxDydw2Ap0Wb0s7ztyb_SZ4",
    'Content-Type': 'application/json'
}
body={
    "review":"nice course",
    'rating':3
}
get_response=requests.post(endpoint,json=body,headers=headers)

def respons(payload:Comment):
   
    print(payload.review)
   

U=from_dict(data_class=Comment,data=get_response.json())
respons(U)