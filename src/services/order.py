from django.db import transaction
from src.apps.orders.models import Order, OrderItem
from src.apps.users.serializers import AuthSerializer
from src.apps.users.models import User
from src.apps.orders.serializers import LocationSerializer, OrderItemSerializer, OrderSerializer
from src.apps.vendors.models import MenuItem
from src.utils.helpers import clean_db_error_msgs

# order 
def orderListService():
    try:
        objs = Order.objects.all()
        serializer = OrderSerializer(instance=objs, many=True)
        if serializer:
            return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderService Err] Failed to get order list: {e}")
        return False, clean_db_error_msgs(str(e)), None
    
def createOrderService(requestData):
    try:
        customer = requestData.get("customer", None)
        menuItems = requestData.get("menuItems", [])

        with transaction.atomic():
            if customer is not None:
                import uuid
                fname = customer["first_name"]
                lname = customer["last_name"]
                email = f"{fname}.{lname}{str(uuid.uuid4())[:6]}@gmail.com"
                phone = customer["phone"]
                specialNotes=customer.get("specialNotes", "")

                user_serializer = AuthSerializer(data={
                    "first_name": fname,
                    "last_name": lname,
                    "email": email,
                    "phone": phone,
                    "password": f"secureuser@{phone}",
                    "userType": "customer"
                })
                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
                    user = user_serializer.data

                if menuItems is not None:
                    order_data = {"customer": dict(user).get("id"), "specialNotes": specialNotes}
                    order_serializer = OrderSerializer(data=order_data)
                    if order_serializer.is_valid(raise_exception=True):
                        order = order_serializer.save()
                        order_id = getattr(order, "id")

                        [item.update({"order": order_id, "menuItem": item["id"], "quantity": item["quantity"]}) for item in menuItems]
                        orderitem_serializer = OrderItemSerializer(data=menuItems, many=True)
                        if orderitem_serializer.is_valid(raise_exception=True):
                            orderitem_serializer.save()

                        # location
                        location_serializer = LocationSerializer(data={"order": order_id})
                        if location_serializer.is_valid(raise_exception=True):
                            location_serializer.save()

            return True, "success", None
    except Exception as e:
        print(f"[OrderService Err] Failed to create order: {e}")
        return False, clean_db_error_msgs(str(e)), None

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

