# Generated by Django 3.2.4 on 2021-06-10 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210609_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='recipient_info',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.recipientinfo'),
        ),
    ]
