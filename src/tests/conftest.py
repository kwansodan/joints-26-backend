import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

@pytest.fixture
def auth_headers(db):
    user = User.objects.create_user(
        email="contract@test.com",
        password="password123"
    )

    token = AccessToken.for_user(user)

    return {
        "Authorization": f"Bearer {str(token)}"
    }
