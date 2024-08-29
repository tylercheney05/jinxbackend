# Generated by Django 4.2.11 on 2024-08-06 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_prepared_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.AddField(
            model_name='order',
            name='order_name',
            field=models.CharField(choices=[('Champagne Papi', 'Champagne Papi'), ('Beyoncé', 'Beyoncé')], default='Champagne Papi', max_length=50),
            preserve_default=False,
        ),
    ]
