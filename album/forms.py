from django import forms
from .models import Calendar, Comment
from django.forms.widgets import SelectDateWidget

class CalendarForm(forms.ModelForm):
    date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))

    class Meta:
        model = Calendar
        fields = (
            'title',
            'description',
            'image',
        )

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Write a comment..."
        }
    ))
    class Meta:
        model = Comment
        fields = ('comment',)
