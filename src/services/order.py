from django.db import transaction

from src.apps.orders.models import Order, OrderItem
from src.apps.orders.serializers import (
    LocationSerializer,
    OrderItemSerializer,
    OrderSerializer,
)
from src.apps.payments.serializers import PaymentSerializer
from src.apps.users.models import User
from src.apps.users.serializers import AuthSerializer
from src.apps.vendors.models import MenuItem
from src.utils.helpers import clean_db_error_msgs
from src.utils.workers import clean_email


# order
def orderListService():
    try:
        objs = Order.objects.all()
        serializer = OrderSerializer(instance=objs, many=True)
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
                specialNotes = customer.get("specialNotes", "")

                user_serializer = AuthSerializer(
                    data={
                        "first_name": fname,
                        "last_name": lname,
                        "email": clean_email(email),
                        "phone": phone,
                        "password": f"secureuser@{phone}",
                        "userType": "customer",
                    }
                )
                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
                    user = user_serializer.data

                if menuItems is not None:
                    # order
                    order_data = {
                        "customer": dict(user).get("id"),
                        "specialNotes": specialNotes,
                    }
                    order_serializer = OrderSerializer(data=order_data)
                    if order_serializer.is_valid(raise_exception=True):
                        order = order_serializer.save()
                        order_id = getattr(order, "id")

                        # orderitem
                        [
                            item.update(
                                {
                                    "order": order_id,
                                    "menuItem": item["id"],
                                    "quantity": item["quantity"],
                                }
                            )
                            for item in menuItems
                        ]
                        orderitem_serializer = OrderItemSerializer(
                            data=menuItems, many=True
                        )
                        if orderitem_serializer.is_valid(raise_exception=True):
                            orderitem_serializer.save()

                        # location
                        location_serializer = LocationSerializer(
                            data={"order": order_id}
                        )
                        if location_serializer.is_valid(raise_exception=True):
                            location_serializer.save()

                        # payment
                        # payment_serializer = PaymentSerializer(data={"order": order_id})
                        # if payment_serializer.is_valid(raise_exception=True):
                        #     payment_serializer.save()

            return True, "success", None
    except Exception as e:
        print(f"[OrderService Err] Failed to create order: {e}")
        return False, "failed", None


def getOrderDetailService(pk):
    try:
        obj = Order.objects.get(pk=pk)
        if obj:
            serializer = OrderSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderService Err] Failed to get order detail: {e}")
        return False, "failed", None


def updateOrderDetailService(pk, requestData):
    try:
        customer = requestData.get("customer", None)
        orderUpdates = requestData.get("orderUpdates", None)
        newOrders = requestData.get("newOrders", None)
        subordersToRemove = requestData.get("subordersToRemove", None)

        with transaction.atomic():
            try:
                obj = Order.objects.get(pk=pk)
            except Exception as e:
                return False, "Order not found", None

            if customer is not None:
                # customer = User.objects.filter(pk=customer["id"]).update(
                #     first_name=customer["first_name"],
                #     last_name=customer["last_name"],
                #     phone=customer["phone"],
                # )
                user_serializer = AuthSerializer(
                    instance=customer, data=customer, partial=True
                )
                if user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()

            if orderUpdates is not None and len(orderUpdates) > 0:
                [item.update({"order": obj.id}) for item in orderUpdates]
                for item in orderUpdates:
                    orderitem_instance = OrderItem.objects.get(
                        pk=item["menuItemId"], order=obj
                    )
                    orderitem_serializer = OrderItemSerializer(
                        instance=orderitem_instance, data=item, partial=True
                    )
                    if orderitem_serializer.is_valid(raise_exception=True):
                        orderitem_serializer.save()

                # order_serializer = OrderSerializer(instance)
                # for item in orderUpdates:
                #     if orderitem:
                #         orderitem.quantity = (
                #             item["quantity"] if item["quantity"] else orderitem.quantity
                #         )
                #         orderitem.save()

            if len(newOrders) > 0:
                for item in newOrders:
                    # menuItem = MenuItem.objects.get(pk=item["menuItemId"])
                    # OrderItem.objects.create(
                    #     order=obj, menuItem=menuItem, quantity=item["quantity"]
                    # )
                    new_orderitem_serializer = OrderItemSerializer(
                        data={
                            "order": obj,
                            "menuItem": item["menuItemId"],
                            "quantity": item["quantity"],
                        }
                    )
                    if new_orderitem_serializer.is_valid(raise_exception=True):
                        new_orderitem_serializer.save()

            if len(subordersToRemove) > 0:
                for item in subordersToRemove:
                    print("removing item", item)
                    orderobj = OrderItem.objects.get(pk=item, order=obj)
                    if orderobj:
                        orderobj.delete()
                    else:
                        return False, "sub order item not found", None

            return True, "success", None
    except Exception as e:
        print(f"[OrderService Err] Failed to update order: {e}")
        return False, "failed", None


def deleteOrderService(pk):
    try:
        obj = Order.objects.get(pk=pk)
        if obj:
            obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[OrderService Err] Failed to delete order: {e}")
        return False, "failed", None
