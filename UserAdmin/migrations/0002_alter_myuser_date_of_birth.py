# Generated by Django 5.0.6 on 2024-06-26 03:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2004, 6, 26)),
        ),
    ]
