# Generated by Django 5.1.2 on 2024-12-26 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='city',
        ),
        migrations.RemoveField(
            model_name='location',
            name='is_event',
        ),
        migrations.RemoveField(
            model_name='location',
            name='state',
        ),
        migrations.RemoveField(
            model_name='location',
            name='zip_code',
        ),
    ]
