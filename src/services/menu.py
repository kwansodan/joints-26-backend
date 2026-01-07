from src.apps.menu.models import Menu 
from src.apps.menu.serializers import MenuSerializer

# users
def menuListService():
    status = False
    message = "Error fetching menus" 
    data = None
    try:
        objs = Menu.objects.all()
        serializer = MenuSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[MenuService Err] Failed to get menu list: {e}")
    return status, message, data
    
def createMenuService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Menu created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[MenuService Err] Failed to create menu: {e}")
    return status, message, data

def getMenuDetailService(pk):
    status = False
    message = "no menu found"
    data = None
    try:
       obj = Menu.objects.get(pk=pk)
       if obj:
            serializer = MenuSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[MenuService Err] Failed to get menu detail: {e}")
    return status, message, data

def updateMenuDetailService(pk, requestData):
    status = False
    message = "menu does not exists" 
    data = None
    try:
        obj = Menu.objects.get(pk=pk)
        if obj:
            serializer = MenuSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[MenuService Err] Failed to update menu: {e}")
    return status, message, data

def deleteMenuService(pk):
    status = False
    message = "menu doest not exists" 
    data = None
    try:
        obj = Menu.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[MenuService Err] Failed to delete menu: {e}")
    return status, message, data
