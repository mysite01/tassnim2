from django import forms
from .models import HolidayHousing, Comment


class HolidayHousingForm(forms.ModelForm):
    class Meta:
        model = HolidayHousing

        fields = ['title', 'type', 'costs', 'location', 'rooms', 'specials']

        widgets = {
            'type': forms.Select(choices=HolidayHousing.TYPE),
            'costs': forms.Select(choices=HolidayHousing.COSTS),
            'location': forms.Select(choices=HolidayHousing.LOCATION),
            'user': forms.HiddenInput(),
            'myuser': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['text']

        widgets = {
            'myuser': forms.HiddenInput(),
            'holiday_housing': forms.HiddenInput(),
            'timestamp': forms.HiddenInput(),
        }


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
