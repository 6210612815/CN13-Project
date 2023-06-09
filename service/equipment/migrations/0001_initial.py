# Generated by Django 4.2 on 2023-04-25 15:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=1000)),
                ('pic', models.ImageField(upload_to='images/')),
                ('available', models.BooleanField(default=True)),
                ('picked', models.IntegerField(default=0)),
                ('create_datetime', models.DateTimeField(default=datetime.datetime(2023, 4, 25, 22, 15, 0, 678074))),
                ('category', models.CharField(choices=[('Laptops', 'Laptops'), ('Mouse', 'Mouse'), ('Keyboards', 'Keyboards'), ('Monitors', 'Monitors'), ('Speaker', 'Speaker'), ('Headsets', 'Headsets')], max_length=20)),
                ('own', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.student')),
            ],
        ),
    ]
