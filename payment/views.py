from rest_framework.views import APIView
from .serializers import InputSerializer,TransactionOrderSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .transaction import Transactions
from .services import PaymentServices
from rest_framework.generics import CreateAPIView
from .services import WebhookService
from .models import TransactionLog
from rest_framework.exceptions import NotFound
from utils.error_handler import error_handler


class InitailizesTrasactionApiView(CreateAPIView):
    serializer_class=InputSerializer
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    

    def post(self, request, format=None,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=PaymentServices().initialize_transaction(payload=serializer.data,user=self.request.user)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED,headers=headers)


class VerifyTransactionApiView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    
    def get(self, request, *args, **kwargs):
        user=self.request.user
        data=PaymentServices().verify_transaction(self.kwargs['pk'])
        if data['data']['status']=='success':
            transactions=Transactions()
            transactions.log_customer(data['data'],user)
            context=transactions.log_transaction(transaction_data=data['data'],user=user)
        return Response(context,status=status.HTTP_200_OK)
    


class WebhookHookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        webhook_service = WebhookService(request)
        context=webhook_service.webhook_handler()
        return Response(context,status=status.HTTP_200_OK)


class TransactionOrderApiView(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        try:
            get_user_order=TransactionLog.objects.select_related("course","user").filter(user=self.request.user).all()
            order=TransactionOrderSerializer(get_user_order,many=True)
        except Exception as e:
            raise NotFound(error_handler(e))
        return Response(order.data,status=status.HTTP_200_OK)