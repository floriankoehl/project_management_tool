# Generated by Django 5.2.4 on 2025-08-01 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0022_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='order_counter',
            field=models.IntegerField(default=0),
        ),
    ]
