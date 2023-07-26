from django import forms
from django.core.exceptions import ValidationError

from ark.utils import parse_ark


def validate_shoulder(shoulder: str):
    if not shoulder.startswith("/"):
        raise ValidationError("Shoulders must start with a forward slash")


def validate_ark(ark: str):
    try:
        parse_ark(ark)
    except ValueError as e:
        raise ValidationError(f"Invalid ARK: {e}")


class MintArkForm(forms.Form):
    naan = forms.IntegerField()
    shoulder = forms.CharField(validators=[validate_shoulder])
    url = forms.URLField(required=False)
    metadata = forms.CharField(required=False)
    title = forms.CharField(required=False)
    type = forms.CharField(required=False)
    commitment = forms.CharField(required=False)
    identifier = forms.CharField(required=False)
    format = forms.CharField(required=False)
    relation = forms.CharField(required=False)
    source = forms.URLField(required=False)


class UpdateArkForm(forms.Form):
    ark = forms.CharField(validators=[validate_ark])
    url = forms.URLField(required=False)
    metadata = forms.CharField(required=False)
    title = forms.CharField(required=False)
    type = forms.CharField(required=False)
    commitment = forms.CharField(required=False)
    identifier = forms.CharField(required=False)
    format = forms.CharField(required=False)
    relation = forms.CharField(required=False)
    source = forms.URLField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        # Remove fields that are not provided in the request
        for field_name in self.fields:
            if field_name not in self.data:
                cleaned_data.pop(field_name, None)

        return cleaned_data