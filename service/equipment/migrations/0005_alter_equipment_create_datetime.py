# Generated by Django 4.2 on 2023-04-25 17:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_alter_equipment_create_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='create_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 26, 0, 22, 40, 907755)),
        ),
    ]
