from django.db import models
from django.contrib.auth import get_user_model

from car_rental import settings
from cars.models import Car


User = get_user_model()


class Like(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['car', 'owner']


class Favourites(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')

    class Meta:
        unique_together = ['car', 'user']
