# Generated by Django 5.1.2 on 2024-10-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_app', '0009_rename_prodcut_cart_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
