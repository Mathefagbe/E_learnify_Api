from django.urls import path as url
from .views import (InitailizesTrasactionApiView,VerifyTransactionApiView,WebhookHookView,TransactionOrderApiView)


urlpatterns = [
    url('paystack/transaction/initiate',InitailizesTrasactionApiView.as_view(),name='initiate_transaction'),
    url('paystack/transaction/verify/<pk>',VerifyTransactionApiView.as_view(),name='verify_transaction'),
    url('paystack/transaction/webhook',WebhookHookView.as_view(),name='webhook_verification'),
    url('orders/',TransactionOrderApiView.as_view(),name='Transaction_orders'),
]