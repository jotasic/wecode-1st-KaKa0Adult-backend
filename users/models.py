from django.db import models
from .managers import ProductManager

class User(models.Model):
    nickname     = models.CharField(max_length=30, unique=True)
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, unique=True)
    gender       = models.CharField(max_length=5)
    birth        = models.CharField(max_length=12)
    like         = models.ManyToManyField('products.Product', through='Like')

    objects = models.Manager()
    manager = ProductManager()
    
    class Meta:
        db_table = 'users'

class Like(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='origin_like')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'