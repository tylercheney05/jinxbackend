# Generated by Django 4.2.11 on 2024-10-10 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flavors', '0001_initial'),
        ('sodas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LimitedTimePromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('soda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='sodas.soda')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemFlavor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('flavor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_item_flavors', to='flavors.flavor')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flavors', to='menuitems.menuitem')),
            ],
        ),
        migrations.CreateModel(
            name='LimitedTimeMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limited_time_promo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menuitems.limitedtimepromotion')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='limited_time_promotions', to='menuitems.menuitem')),
            ],
        ),
    ]
