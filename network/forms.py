from django import forms
from django.forms import Textarea

from .models import User, New_Post

# Very basic new_post_form
# TODO: add more to the form potentially will have to do that after making more classes
class new_post_form(forms.ModelForm):
    class Meta:
        model = New_Post
        field = "__all__"
        exclude = ["user"]  # TODO: also add post_id here when that is made
        widgets = {
            "comment_field": Textarea(
                attrs={
                    "style": "height: 100px; width: 100%; resize: initial;",
                    "class": "form-control",
                }
            )
        }
