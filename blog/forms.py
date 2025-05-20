from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content',
            'featured_image', 'meta_description', 'is_published'
        ] 