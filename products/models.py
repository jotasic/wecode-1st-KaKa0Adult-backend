from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Character(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'characters'

class Product(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.CASCADE)
    character  = models.ForeignKey(Character, on_delete=models.CASCADE)
    name       = models.CharField(max_length=45)
    stock      = models.IntegerField()
    sell_count = models.IntegerField()
    price      = models.DecimalField(max_digits=9, decimal_places=3)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'

class ImageUrl(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url     = models.CharField(max_length=2000)
  
    class Meta:
        db_table = 'image_urls'

class Review(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    star_point = models.SmallIntegerField()
    content    = models.TextField(blank=True)

    class Meta:
        db_table = 'reviews'