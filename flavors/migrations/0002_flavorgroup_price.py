# Generated by Django 4.2.11 on 2024-06-27 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flavors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flavorgroup',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=5),
            preserve_default=False,
        ),
    ]
