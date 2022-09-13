from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from user.views import LoginApiView
from rest_framework.routers import SimpleRouter
from rest_framework import permissions
from user.views import home
from cars.views import CarViewSet
from categories.views import CategoryViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib.auth.views import LogoutView, LoginView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = SimpleRouter()
router.register('cars', CarViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', home, name='home'),
    path('api/v1/', include(router.urls)),
    path('api/v1/user/', include('user.urls')),
    path('accounts/', include('allauth.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
