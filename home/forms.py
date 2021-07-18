from django import forms
from home import models

class PostForm(forms.ModelForm):
    class Meta:
        model=models.Post
        fields=['content', 'image']
    def save(self, commit=True):   
        return super().save(commit=commit)


class PostComment(forms.ModelForm):
    class Meta:
        model=models.Comment
        fields=['content']

