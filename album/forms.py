from django import forms
from .models import Calendar, Comment, Image, ImageComment
from bootstrap_datepicker_plus import DatePickerInput

class CalendarForm(forms.ModelForm):

    class Meta:
        model = Calendar
        fields = (
            'title',
            'description',
            'date',
            'emoticon'
        )
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d')
        }

class CommentForm(forms.ModelForm):
    # comment = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': "Write a comment..."
    #     }
    # ))
    class Meta:
        model = Comment
        fields = ('comment',)



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = (
            'description',
            'image',
        )

class ImageCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Write a comment..."
        }
    ))
    class Meta:
        model = ImageComment
        fields = ('comment',)
