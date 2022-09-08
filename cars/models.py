from django.db import models
from categories.models import Category


class Car(models.Model):
    title = models.CharField(max_length=100)
    seats = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} - - - Цена за сутки: {self.price}'
