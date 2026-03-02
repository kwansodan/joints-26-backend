from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.conf.urls.static import static
from src.apps.users.views.auth_login import LoginView, RefreshTokenView

urlpatterns = [
    path("admin/interface/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-docs",
    ),
    path("auth/login/", LoginView.as_view(), name="signin"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("bikers/", include("src.apps.bikers.urls")),
    path("users/", include("src.apps.users.urls")),
    path("vendors/", include("src.apps.vendors.urls")),
    path("orders/", include("src.apps.orders.urls")),
    path("payments/", include("src.apps.payments.urls")),
    path("notifications/", include("src.apps.notifications.urls")),
    path("external/", include("src.apps.external.urls")),
    path("reports/", include("src.apps.reports.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
