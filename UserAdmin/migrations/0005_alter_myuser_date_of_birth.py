# Generated by Django 4.2 on 2024-07-14 14:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAdmin', '0004_myuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2004, 7, 14)),
        ),
    ]
