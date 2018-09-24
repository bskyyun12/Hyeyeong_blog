from django import forms
from .models import Calendar, Comment

class CalendarForm(forms.ModelForm):

    class Meta:
        model = Calendar
        fields = (
            'title',
            'description',
            'image',
            'date',
            'emoticon'
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
