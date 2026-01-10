from src.apps.orders.models import OrderItem
from src.apps.orders.serializers import OrderItemSerializer

# biker 
def orderItemListService():
    status = False
    message = "Error fetching order items" 
    data = None
    try:
        objs = OrderItem.objects.all()
        serializer = OrderItemSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[OrderItemService Err] Failed to get order item list: {e}")
    return status, message, data
    
def createOrderItemService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Order item created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[OrderItemService Err] Failed to create order item: {e}")
    return status, message, data

def getOrderItemDetailService(pk):
    status = False
    message = "no order item found"
    data = None
    try:
       obj = OrderItem.objects.get(pk=pk)
       if obj:
            serializer = OrderItemSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[OrderItemService Err] Failed to get order item detail: {e}")
    return status, message, data

def updateOrderItemDetailService(pk, requestData):
    status = False
    message = "order item does not exists" 
    data = None
    try:
        obj = OrderItem.objects.get(pk=pk)
        if obj:
            serializer = OrderItemSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[OrderItemService Err] Failed to update order item: {e}")
    return status, message, data

def deleteOrderItemService(pk):
    status = False
    message = "order item doest not exists" 
    data = None
    try:
        obj = OrderItem.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[OrderItemService Err] Failed to delete order item: {e}")
    return status, message, data

