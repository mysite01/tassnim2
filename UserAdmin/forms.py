from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class MySignUpForm(UserCreationForm):

    class Meta:

        model = MyUser

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
            'date_of_birth',
            'profile_image',
            'some_file'
            # password field is not explicitly need, as provided by UserCreationForm
        )
