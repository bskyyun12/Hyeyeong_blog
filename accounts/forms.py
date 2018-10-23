from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, BabyProfile
from accounts.models import User
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

# class EntryForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     date = forms.DateTimeField()
#     description = forms.CharField(widget=forms.Textarea)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'email',
            'password1',
            'password2',
        )
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.is_active = False

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
        )

class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'description',
            'city',
            'website',
            'phone',
            'image',
        )

class BabyForm(forms.ModelForm):
    birthday = forms.SplitDateTimeField()
    class Meta:
        model = BabyProfile
        fields = (
            'image',
            'first_name',
            'last_name',
            'birthday',
            'born_weight',
            'born_height',
            'born_location',
        )
    def __init__(self, *args, **kwargs):
        super(BabyForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget.widgets[0]=DatePickerInput(format='%Y-%m-%d')
        self.fields['birthday'].widget.widgets[1]=TimePickerInput(format='%H:%M')
