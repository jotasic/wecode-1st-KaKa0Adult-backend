from django.db import models

class OrderStatus(models.Model):
    BASKET  = 1
    PAYMENT = 2

    status = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_statuses'

class Order(models.Model):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status   = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    recipient_info = models.OneToOneField('RecipientInfo', on_delete=models.CASCADE, null=True)
    order_time     = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    count    = models.IntegerField()
    selected = models.BooleanField(default=True)

    class Meta:
        db_table = 'order_items'
    
class RecipientInfo(models.Model):
    address      = models.CharField(max_length=100)
    name         = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=15)
    request      = models.CharField(max_length=100)

    class Meta:
        db_table = 'recipient_infoes'