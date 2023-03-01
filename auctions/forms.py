from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Comment
        fields = ('content',)