from django import forms
from .models import Post, Comment, Car


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={'class': 'form_control'})}


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostSearchInput(forms.Form):
    search = forms.CharField()


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

