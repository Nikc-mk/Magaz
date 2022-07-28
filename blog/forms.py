from django import forms
from .models import Comment


class CommentForm(forms.Form):
    name = forms.CharField
    text = forms.CharField(widget=forms.Textarea)
    post = forms.CharField
