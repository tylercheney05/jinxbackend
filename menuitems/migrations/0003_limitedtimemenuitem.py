# Generated by Django 4.2.11 on 2024-09-30 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menuitems', '0002_limitedtimepromotion'),
    ]

    operations = [
        migrations.CreateModel(
            name='LimitedTimeMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limited_time_promo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menuitems.limitedtimepromotion')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='limited_time_promotions', to='menuitems.menuitem')),
            ],
        ),
    ]
