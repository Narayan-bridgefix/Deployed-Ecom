# Generated by Django 5.1.2 on 2024-10-14 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_app', '0016_remove_order_tracking_product_order_tracking_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_details',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecom_app.ordermodel'),
        ),
        migrations.AddField(
            model_name='payment_details',
            name='pay_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
