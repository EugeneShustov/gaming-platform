from django import forms
from core.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'content', 'rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i}/10') for i in range(1, 11)])
        }
