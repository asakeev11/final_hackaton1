from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from likes_favourites.models import Like, Favourites
from . import serializers
from .models import Car
from rating.serializers import ReviewSerializer
from likes_favourites.serializers import LikeSerializer


class StandartResultsPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandartResultsPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('title',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CarsListSerializer
        return serializers.CarDetailSerializer

    @action(['GET', 'POST'], detail=True)
    def comments(self, request, pk=None):
        car = self.get_object()
        if request.method == 'GET':
            reviews = car.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return Response(serializer, status=200)
        data = request.data
        serializer = ReviewSerializer(data=data, context={'request': request, 'car': car})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def get_permissions(self):
        # Лайкать , добавлять в избранное может аутентифицированный юзер
        if self.action in ('like', 'unlike', 'favourite'):
            return [permissions.IsAuthenticated()]
        # Изменять, создавать и удалять может только админ
        elif self.action in ('update', 'partial_update', 'destroy', 'create', 'get_likes'):
            return [permissions.IsAdminUser()]
        # Просматривать могут все
        else:
            return [permissions.AllowAny(), ]

    @action(['POST'], detail=True)
    def like(self, request, pk):
        car = self.get_object()
        if request.user.liked.filter(car=car).exists():
            return Response('You have already liked  this product', status=400)
        Like.objects.create(car=car, owner=request.user)
        return Response('You liked', status=201)

    # UNLIKE
    @action(['POST'], detail=True)
    def unlike(self, request, pk):
        car = self.get_object()
        if not request.user.liked.filter(car=car).exists():
            return Response('You have not liked this product yet', status=400)
        request.user.liked.filter(car=car).delete()
        return Response('You unliked this product', status=204)

    # Список лайкнувших юзеров может посмотреть только админ
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)

    # Добавление в избранное
    @action(['POST'], detail=True)
    def favourite(self, request, pk):
        car = self.get_object()
        if request.user.favourites.filter(car=car).exists():
            request.user.favourites.filter(car=car).delete()
            return Response('Removed from favourites', status=204)
        Favourites.objects.create(car=car, user=request.user)
        return Response('Added to Favourites', status=201)
