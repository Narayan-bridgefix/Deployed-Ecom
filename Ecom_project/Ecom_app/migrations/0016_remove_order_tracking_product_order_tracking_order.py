# Generated by Django 5.1.2 on 2024-10-14 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_app', '0015_order_tracking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_tracking',
            name='product',
        ),
        migrations.AddField(
            model_name='order_tracking',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ecom_app.ordermodel'),
        ),
    ]
