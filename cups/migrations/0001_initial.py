# Generated by Django 4.2.11 on 2024-06-27 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('16', '16 oz'), ('32', '32 oz')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]