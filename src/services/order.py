from src.apps.orders.models import Order
from src.apps.orders.serializers import OrderSerializer

# biker 
def orderListService():
    status = False
    message = "Error fetching orders" 
    data = None
    try:
        objs = Order.objects.all()
        serializer = OrderSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[OrderService Err] Failed to get order list: {e}")
    return status, message, data
    
def createOrderService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "order created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[OrderService Err] Failed to create order: {e}")
    return status, message, data

def getOrderDetailService(pk):
    status = False
    message = "no order found"
    data = None
    try:
       obj = Order.objects.get(pk=pk)
       if obj:
            serializer = OrderSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[OrderService Err] Failed to get order detail: {e}")
    return status, message, data

def updateOrderDetailService(pk, requestData):
    status = False
    message = "order does not exists" 
    data = None
    try:
        obj = Order.objects.get(pk=pk)
        if obj:
            serializer = OrderSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[OrderService Err] Failed to update order: {e}")
    return status, message, data

def deleteOrderService(pk):
    status = False
    message = "order doest not exists" 
    data = None
    try:
        obj = Order.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[OrderService Err] Failed to delete order: {e}")
    return status, message, data

