from rest_framework import serializers
from .models import Like, Favourites
from cars.serializers import CarsListSerializer


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner',)


# FAVOURITES
class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('car',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['car'] = CarsListSerializer(instance.car).data
        return repr
