from pprint import pprint

from django.core.validators import validate_email
from django.db import transaction

from src.apps.orders.models import Order, OrderItem
from src.apps.orders.serializers import (
    OrderLocationSerializer,
    OrderItemSerializer,
    OrderSerializer,
)
from src.apps.payments.models import PaystackTransactionReference
from src.apps.payments.serializers import (
    PaymentSerializer,
    PaystackTransactionReferenceSerializer,
)
from src.apps.users.models import Customer, User
from src.apps.users.serializers import AuthSerializer, CustomerSerializer
from src.apps.vendors.models import MenuItem
from src.utils.helpers import clean_db_error_msgs
from src.utils.workers import clean_email, verify_location_capture_link


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

                try:
                    validate_email(customer["email"])
                except Exception as e:
                    return False, "Invalid email", None

                fname = customer["first_name"]
                lname = customer["last_name"]
                email = customer["email"]
                phone = customer["phone"]
                specialNotes = customer.get("specialNotes", "")

                customer_serializer = CustomerSerializer(
                    data={
                        "first_name": fname,
                        "last_name": lname,
                        "email": email,
                        "phone": phone,
                    }
                )
                if customer_serializer.is_valid(raise_exception=True):
                    customer_serializer.save()
                    customer = customer_serializer.data

                if menuItems is not None:
                    # order
                    order_data = {
                        "customer": dict(customer).get("id"),
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

                        # update order subtotal
                        order.update_order_subtotal

                        # location
                        order_location_serializer = OrderLocationSerializer(
                            data={"order": order_id}
                        )
                        if order_location_serializer.is_valid(raise_exception=True):
                            order_location_serializer.save()

                        # payment transaction ref object
                        paystack_trx_ref_obj_serializer = (
                            PaystackTransactionReferenceSerializer(
                                data={
                                    "order": order_id,
                                    "reference": "",
                                    "paymentLink": "",
                                    "processed": False,
                                }
                            )
                        )
                        if paystack_trx_ref_obj_serializer.is_valid(
                            raise_exception=True
                        ):
                            paystack_trx_ref_obj_serializer.save()

            return True, "success", None
    except Exception as e:
        print(f"[OrderService Err] Failed to create order: {e}")
        return False, "failed", None


def getOrderDetailService(pk):
    try:
        print("from this service")
        # token_valid = verify_location_capture_link(token=token, category="order")
        # if not token_valid:
        #     return False, "Invalid link", None

        obj = Order.objects.get(pk=pk)
        serializer = OrderSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderService Err] Failed to get order detail: {e}")
        return False, "Invalid link", None


def updateOrderDetailService(pk, requestData):
    try:
        customer = requestData.get("customer", None)
        orderUpdates = requestData.get("orderUpdates", None)
        newOrders = requestData.get("newOrders", None)
        subordersToRemove = requestData.get("subordersToRemove", None)

        with transaction.atomic():
            try:
                order = Order.objects.get(pk=pk)
            except Exception as e:
                return False, "Order not found", None

            if customer is not None:
                customerObj = Customer.objects.get(id=order.customer.id)
                customer_serializer = CustomerSerializer(
                    instance=customerObj, data=customer, partial=True
                )
                if customer_serializer.is_valid(raise_exception=True):
                    customer_serializer.save()

            if orderUpdates is not None and len(orderUpdates) > 0:
                [item.update({"order": order.id}) for item in orderUpdates]
                for item in orderUpdates:
                    orderitem_instance = OrderItem.objects.get(
                        pk=item["menuItemId"], order=order
                    )
                    orderitem_serializer = OrderItemSerializer(
                        instance=orderitem_instance, data=item, partial=True
                    )
                    if orderitem_serializer.is_valid(raise_exception=True):
                        orderitem_serializer.save()

            if len(newOrders) > 0:
                for item in newOrders:
                    # menuItem = MenuItem.objects.get(pk=item["menuItemId"])
                    # OrderItem.objects.create(
                    #     order=obj, menuItem=menuItem, quantity=item["quantity"]
                    # )
                    new_orderitem_serializer = OrderItemSerializer(
                        data={
                            "order": order,
                            "menuItem": item["menuItemId"],
                            "quantity": item["quantity"],
                        }
                    )
                    if new_orderitem_serializer.is_valid(raise_exception=True):
                        new_orderitem_serializer.save()

            if len(subordersToRemove) > 0:
                for item in subordersToRemove:
                    print("removing item", item)
                    orderobj = OrderItem.objects.get(pk=item, order=order)
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
