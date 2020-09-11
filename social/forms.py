from django import forms
from social import models
#it is deriving from moels so we can make it a model form
class PostForm(forms.ModelForm):
    class Meta:
        model=models.Post
        fields=['content', 'image']  #defining which fields we want to create
# overwriting save method
    def save(self, commit=True):   #commit actually saves the data to databases
        return super().save(commit=commit)


class PostComment(forms.ModelForm):
    class Meta:
        model=models.Comment
        fields=['content']

