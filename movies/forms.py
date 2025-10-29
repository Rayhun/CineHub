from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Simple visitor comment form rendered on the movie detail page."""

    class Meta:
        model = Comment
        fields = ("name", "body")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Name",
                    "required": True,
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Your Comment...",
                    "required": True,
                }
            ),
        }
