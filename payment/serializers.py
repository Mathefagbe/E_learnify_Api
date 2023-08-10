from rest_framework import serializers
from .models import PayStackCustomer,TransactionLog

class UserPaymentInfoSerializer(serializers.ModelSerializer):
    pass

class InputSerializer(serializers.Serializer):
    amount=serializers.DecimalField(max_digits=10,decimal_places=2)
    course_id=serializers.UUIDField()
 
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayStackCustomer
        fields = "__all__"
