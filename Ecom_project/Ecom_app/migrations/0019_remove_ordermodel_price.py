# Generated by Django 5.1.2 on 2024-10-14 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_app', '0018_ordermodel_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='price',
        ),
    ]
