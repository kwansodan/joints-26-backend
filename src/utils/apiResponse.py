from rest_framework import status
from rest_framework.response import Response

class ApiResponse:
    viewable = ("ok", "created")
    status_maps = {
        "ok": status.HTTP_200_OK,
        "bad": status.HTTP_400_BAD_REQUEST, 
        "created": status.HTTP_201_CREATED,
        "unauthorized": status.HTTP_401_UNAUTHORIZED,
        "not_found": status.HTTP_404_NOT_FOUND,
    }

    def __init__(self, status_key, message, data):
        if not status_key in self.status_maps:
            raise ValueError(f"Invalid status: {status}")
        
        self.status_key = status_key
        self.status = self.status_maps.get(status_key)
        self.message = message or ""
        self.data = data
  
    @property
    def response(self):
        return Response(
            {
                "status": self.status,
                "message": self.message,
                "data": self.data if self.status_key in self.viewable else None
            }, 
            status=self.status
        )

