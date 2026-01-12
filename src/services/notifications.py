from src.apps.notifications.models import Notification 
from src.apps.notifications.serializers import NotificationSerializer

# biker 
def notificationListService():
    status = False
    message = "Error fetching notifications" 
    data = None
    try:
        objs = Notification.objects.all()
        serializer = NotificationSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[NotificationService Err] Failed to get notification list: {e}")
    return status, message, data
    
def createNotificationService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = NotificationSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "notification created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[NotificationService Err] Failed to create notification: {e}")
    return status, message, data

def getNotificationDetailService(pk):
    status = False
    message = "no notification found"
    data = None
    try:
       obj = Notification.objects.get(pk=pk)
       if obj:
            serializer = NotificationSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[NotificationService Err] Failed to get notification detail: {e}")
    return status, message, data

def updateNotificationDetailService(pk, requestData):
    status = False
    message = "notification does not exists" 
    data = None
    try:
        obj = Notification.objects.get(pk=pk)
        if obj:
            serializer = NotificationSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[NotificationService Err] Failed to update notification: {e}")
    return status, message, data

def deleteNotificationService(pk):
    status = False
    message = "notification doest not exists" 
    data = None
    try:
        obj = Notification.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[NotificationService Err] Failed to delete notification: {e}")
    return status, message, data

