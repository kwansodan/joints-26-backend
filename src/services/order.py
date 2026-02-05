from django.db import transaction
from src.apps.orders.models import Order, OrderItem
from src.apps.users.serializers import AuthSerializer
from src.apps.users.models import User
from src.apps.orders.serializers import CreateOrderSerializer, OrderItemSerializer, OrderSerializer
from src.apps.vendors.models import MenuItem

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
            requestCopy = requestData.copy()
            customer = requestCopy.get("customer", None)
            menuItems = requestCopy.get("menuItems", [])

            if customer is not None:
                import uuid
                fname = customer["first_name"]
                lname = customer["last_name"]
                email = f"{fname}.{lname}{str(uuid.uuid4())[:6]}@gmail.com"
                phone = customer["phone"]
                password=f"{fname}@{phone[:4]}"
                specialNotes=customer.get("specialNotes", "")

                user_serializer = AuthSerializer(data={
                    "first_name": fname,
                    "last_name": lname,
                    "email": email,
                    "phone": phone,
                    "password": password,
                    "userType": "customer"
                })
                if user_serializer.is_valid():
                    user_serializer.save()
                    user = user_serializer.data
                else:
                    return False, f"{user_serializer.errors}", None

                if menuItems is not None:
                    order_data = {"customer": dict(user)["id"]}
                    order_serializer = CreateOrderSerializer(data=order_data)
                    if order_serializer.is_valid():
                        order = order_serializer.save()
                    else:
                        return False, f"{order_serializer.errors}", None

                    for item in menuItems:
                        orderitem_serializer = OrderItemSerializer(data={
                            "order": order.pk,
                            "menuItem": item["id"],
                            "quantity": item["quantity"],
                            "specialNotes": specialNotes
                        })
                        if orderitem_serializer.is_valid():
                            orderitem_serializer.save()
                        else:
                            print("orderitem serializer errors", orderitem_serializer.errors)
                            return False, f"{orderitem_serializer.error_messages}", None

                    status = True
                    data = order_serializer.data
                    message = "order created successfully"
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
        print("request data", requestData)
        with transaction.atomic():
            customer = requestData.get("customer", None)
            orderUpdates = requestData.get("orderUpdates", None)
            newOrders = requestData.get("newOrders", None)
            subordersToRemove = requestData.get("subordersToRemove", None)

            try:
                obj = Order.objects.get(pk=pk)
            except Exception as e:
                return False, "Order not found", None
            
            if customer is not None:
                customer = User.objects.filter(pk=customer["id"]).update(
                    first_name=customer["first_name"],
                    last_name=customer["last_name"],
                    phone=customer["phone"],
                )

            if len(orderUpdates) > 0:
                for item in orderUpdates:
                    orderitem = OrderItem.objects.get(pk=item["menuItemId"], order=obj) 
                    if orderitem:
                        orderitem.quantity = item["quantity"] if item["quantity"]  else orderitem.quantity
                        orderitem.save()

            if len(newOrders) > 0:
                for item in newOrders:
                    menuItem = MenuItem.objects.get(pk=item["menuItemId"])
                    OrderItem.objects.create(
                        order=obj,
                        menuItem=menuItem,
                        quantity=item["quantity"]
                    ) 

            if len(subordersToRemove) > 0:
                for item in subordersToRemove:
                    print("removing item", item)
                    orderobj = OrderItem.objects.get(pk=item, order=obj)
                    if orderobj :
                        orderobj.delete()
                    else:
                        return False, "sub order item not found", None

            status = True
            message = "success" 
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

