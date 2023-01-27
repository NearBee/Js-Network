from django import forms
from django.forms import Textarea

from .models import User, New_Post

# Very basic new_post_form
class new_post_form(forms.ModelForm):
    class Meta:
        model = New_Post
        field = "__all__"
        exclude = ["user", "likes"]
        widgets = {
            "post_field": Textarea(
                attrs={
                    "style": "height: 100px; width: 100%; resize: initial;",
                    "class": "form-control",
                }
            )
        }
