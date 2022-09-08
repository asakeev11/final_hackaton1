from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    car = serializers.ReadOnlyField(source='car.title')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        car = self.context.get('car')
        validated_data['user'] = user
        validated_data['car'] = car
        return super().create(validated_data)

