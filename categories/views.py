from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Category
from .serializers import CategoryListSerializer, CategoryDetailSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategoryDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            permission_classes = (permissions.IsAdminUser,)
        return [permission() for permission in permission_classes]
