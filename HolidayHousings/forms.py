from django import forms
from .models import HolidayHousing, Comment

from django import forms
from .models import Product


class HolidayHousingForm(forms.ModelForm):
    class Meta:
        model = HolidayHousing

        fields = ['title', 'type', 'costs', 'location', 'rooms', 'specials', 'price', 'image', 'max_quantity']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def clean_max_quantity(self):
            max_quantity = self.cleaned_data.get('max_quantity')
            if max_quantity < 1:
                raise forms.ValidationError("Die maximale Stückanzahl muss mindestens 1 sein.")
            return max_quantity

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


class SearchForm(forms.ModelForm):
    title = forms.CharField(required=False)
    rooms = forms.IntegerField(required=False)
    specials = forms.CharField(required=False)

    class Meta:
        model = HolidayHousing
        fields = ['title', 'rooms', 'specials']

