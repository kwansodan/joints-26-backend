from src.apps.orders.models import Order, OrderItem
from src.apps.orders.serializers import OrderSerializer
from src.apps.users.models import User
from src.apps.vendors.models import MenuItem
from django.db import transaction

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
        with transaction.atomic():
            newOrderItems = []
            requestCopy = requestData.copy()
            customer = requestCopy.get("customer", None)
            orderItems = requestCopy.get("orderItems", [])

            if customer is not None:
                import uuid
                customerName = customer["name"].split(" ")
                customerUser = User.objects.create(
                    first_name=customerName[0],
                    last_name=customerName[1] if customerName[1] else "",
                    email=f"{customerName[0]}{str(uuid.uuid4())[:8]}@gmail.com",
                    phone=customer["phone"],
                    userType="customer"
                )

                if orderItems is not None:
                    order = Order.objects.create(customer=customerUser)
                    for item in orderItems:
                        menuItem = MenuItem.objects.get(pk=item["id"])
                        newOrderItem, _ = OrderItem.objects.get_or_create(order=order, menuItem=menuItem, quantity=item["quantity"])
                        newOrderItems.append(newOrderItem)
                    
                status = True
                message = "order created successfully"

            # serializer = OrderSerializer(data=payload, many=True)
            # if serializer.is_valid():
            #     serializer.save()
            #     status = True
            #                 # else:
            #     message = serializer.errors
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

