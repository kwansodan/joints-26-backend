from src.services.users import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.users.permissions import UserModelPermission

class UserListView(BaseAPIView, GenericAPIView):
    serializer_class = AuthSerializer 
    permission_classes = [UserModelPermission]

    def get(self, request):
        success, message, data = usersListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createUserService(request.data)
        return self.created(message, data) if success else self.bad(message)

class UserDetailView(BaseAPIView, GenericAPIView):
    serializer_class = AuthSerializer 
    permission_classes = [UserModelPermission]

    def get(self, request, pk):
        success, message, data = getUserDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateUserService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateUserService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteUserService(pk)
        return self.ok(message, data) if success else self.bad(message)

