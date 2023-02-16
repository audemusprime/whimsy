from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import *


class TitleForm(ModelForm):
    title = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={"cols": 90, "placeholder": "Untitled"}),
    )
    user = forms.HiddenInput()

    class Meta:
        model = Page
        fields = ("title",)


class BlockForm(ModelForm):
    content = forms.CharField(
        label="", required=False, widget=forms.Textarea(attrs={"cols": 90, "rows": 7})
    )

    class Meta:
        model = Block
        fields = ("content",)


BlockFormset = modelformset_factory(
    Block,
    extra=1,
    can_delete=True,
    fields=["content"],
    widgets={
        "content": forms.Textarea(
            attrs={
                "cols": 100,
                "rows": 2,
                "placeholder": "Add a new block",
            }
        )
    },
    labels={"content": ""},
)


class TagForm(ModelForm):
    name = forms.CharField(
        max_length=10,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Create A New Tag"}),
    )

    class Meta:
        model = Tag
        fields = ("name",)
