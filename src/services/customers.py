from secrets import token_urlsafe
from src.apps.users.models import Customer, User
from src.utils.dbOptions import USER_TYPES
from django.contrib.auth.models import Group
from src.apps.users.serializers import CustomerSerializer

# users
def customerListService():
    try:
        customers = Customer.objects.filter(is_staff=False, is_superuser=False)
        serializer = CustomerSerializer(instance=customers, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[CustomerService Err] Failed to get customers list: {e}")
        return False, "failed", None
    
def createCustomerService(requestData):
    try:
        data = requestData.copy()
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[CustomerService Err] Failed to add customer: {e}")
        return False, "failed", None

def getCustomerDetailService(pk):
    try:
        customerObj = Customer.objects.get(pk=pk)
        if not customerObj :
            return False, "No user found", None
        serializer = CustomerSerializer(instance=customerObj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[CustomerService Err] Failed to get user detail: {e}")
        return False, "failed", None

def updateCustomerDetailService(pk, requestData):
    try:
        customer = Customer.objects.get(pk=pk)
        if not customer:
            return False, "no customer found", None

        serializer = CustomerSerializer(instance=customer, data=requestData, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[CustomerService Err] Failed to update user: {e}")
        return False, "failed", None

def deleteCustomerService(userId):
    try:
        user = User.objects.get(pk=userId)
        if not user:
            return False, "no customer found", None
        user.delete()
        return True, "success", None
    except Exception as e:
        print(f"[CustomerService Err] Failed to delete user: {e}")
        return False, "failed", None
