from rest_framework import serializers
from .models import Car
from django.db.models import Avg


class CarsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('title', 'price', 'image')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr


class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def is_liked(self, car):
        user = self.context.get('request').user
        return user.liked.filter(car=car).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes'] = instance.likes.count()
        return repr

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['comments'] = instance.reviews.count()
        return repr
