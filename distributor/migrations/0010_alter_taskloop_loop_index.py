# Generated by Django 5.2.4 on 2025-07-31 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0009_alter_taskloop_scheduled_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskloop',
            name='loop_index',
            field=models.IntegerField(default=1),
        ),
    ]
