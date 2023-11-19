from django import forms

from cybersmart_assessment.todo.utils import get_location_from_string


def validate_location(value: str):
    """Validate the given location.

    If it's possible to create an object using given location definition then it's
    considered valid, otherwise it's not.

    Args:
        value (str): Value to validate.

    Raises:
        forms.ValidationError: If the value is not a valid location definition.
    """
    if get_location_from_string(value) is None:
        raise forms.ValidationError("The value is incorrect.")


class TaskCreateForm(forms.Form):
    """Form for creating task objects."""

    content = forms.CharField(
        label="Task content",
        max_length="200",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "What do you want to do?",
            }
        ),
    )

    location = forms.CharField(
        label="Location",
        required=True,
        widget=forms.Select(
            attrs={
                "id": "locationsDropdown",
                "class": "form-control",
            }
        ),
        validators=[validate_location],
    )
