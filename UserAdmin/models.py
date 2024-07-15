from django.db import models

# Create your models here.
from datetime import datetime, date
import random
from django.contrib.auth.models import User, AbstractUser
from django.db import models


def get_date_20_years_ago():

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    return date(year - 20, month, day)


class MyUser(AbstractUser):
    USER_TYPES = [
        ('SU', 'superuser'),
        ('CS', 'customer support'),
        ('CU', 'customer user'),
        ('QA', 'quality assurance')
    ]

    type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default='CU'
    )

    date_of_birth = models.DateField(default=get_date_20_years_ago())  # default is 20 years old

    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    some_file = models.FileField(upload_to='uploaded_files', blank=True, null=True)

    gets_discount = models.BooleanField(default=False)

    def has_add_permission(self):
        return self.is_superuser or self.is_staff or self.type == 'CS'

    def has_delete_permission(self):
        return self.is_superuser or self.is_staff or self.type == 'CS'

    def has_edit_permission(self):
        return self.is_superuser or self.is_staff or self.type == 'CS'

    def execute_after_login(self):
        # Example implementation; customize as per your logic
        if random.choice([True, False]):
            self.gets_discount = True
            self.save()

    def execute_after_login(self):
        user_gets_randomly_selected_for_discount = random.choice([True, False])

        if user_gets_randomly_selected_for_discount:
            self.gets_discount = True
            self.save()

    def has_birthday_today(self):
        now = datetime.now()
        today_month = now.month
        today_day = now.day

        users_birth_month = self.date_of_birth.month
        users_birth_day = self.date_of_birth.day

        its_the_users_birthday = users_birth_month == today_month and users_birth_day == today_day

        return its_the_users_birthday

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({str(self.date_of_birth)})'
