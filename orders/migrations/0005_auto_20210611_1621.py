# Generated by Django 3.2.4 on 2021-06-11 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_created_at'),
        ('orders', '0004_alter_order_recipient_info'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderList',
            new_name='OrderItem',
        ),
        migrations.AlterModelTable(
            name='orderitem',
            table='order_items',
        ),
    ]