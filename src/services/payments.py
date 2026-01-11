from src.apps.payments.models import Payment 
from src.apps.payments.serializers import PaymentSerializer

# biker 
def paymentListService():
    status = False
    message = "Error fetching payments" 
    data = None
    try:
        objs = Payment.objects.all()
        serializer = PaymentSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[PaymentService Err] Failed to get payment list: {e}")
    return status, message, data
    
def createPaymentService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = PaymentSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "payment created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[PaymentService Err] Failed to create payment: {e}")
    return status, message, data

def getPaymentDetailService(pk):
    status = False
    message = "no payment found"
    data = None
    try:
       obj = Payment.objects.get(pk=pk)
       if obj:
            serializer = PaymentSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[PaymentService Err] Failed to get payment detail: {e}")
    return status, message, data

def updatePaymentDetailService(pk, requestData):
    status = False
    message = "payment does not exists" 
    data = None
    try:
        obj = Payment.objects.get(pk=pk)
        if obj:
            serializer = PaymentSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[PaymentService Err] Failed to update payments: {e}")
    return status, message, data

def deletePaymentService(pk):
    status = False
    message = "payment doest not exists" 
    data = None
    try:
        obj = Payment.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[PaymentService Err] Failed to payment : {e}")
    return status, message, data

