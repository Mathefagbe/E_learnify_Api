from rest_framework import serializers
from .models import TransactionLog


class InputSerializer(serializers.Serializer):
    amount=serializers.DecimalField(max_digits=10,decimal_places=2)
    course_id=serializers.UUIDField()
 

class TransactionOrderSerializer(serializers.ModelSerializer):
    amount=serializers.SerializerMethodField(read_only=True)
    course=serializers.CharField(source="course.title")
    order_id=serializers.CharField(source='txRef')
    payment_status=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=TransactionLog
        fields=['order_id','course','amount','payment_status']

    def get_amount(self,obj:TransactionLog):
        return f"{obj.currency} {obj.amount}"
        
    def get_payment_status(self,obj:TransactionLog):
        return f"Payment {obj.gateway_response}"