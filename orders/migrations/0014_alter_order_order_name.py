# Generated by Django 4.2.11 on 2024-08-28 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_order_order_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='orders.ordername'),
        ),
    ]
