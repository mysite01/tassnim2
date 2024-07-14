# Generated by Django 4.2 on 2024-07-13 21:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HolidayHousings', '0006_commentvote'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('myuser', 'holiday_housing')},
        ),
    ]