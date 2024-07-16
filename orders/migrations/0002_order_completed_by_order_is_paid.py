# Generated by Django 4.2.11 on 2024-07-05 00:36

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completed_by',
            field=cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s_completed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
