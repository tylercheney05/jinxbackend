# Generated by Django 4.2.11 on 2024-07-31 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
