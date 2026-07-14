from django import forms
from django.core.exceptions import ValidationError

from students.models import Student


class FieldControlMixin:
    def field_control_style(self):
        for field in self.fields.values():
            field.widget.attrs.update({ "class": "form-control", "placeholder": f"Enter {field.label.lower()}"})


class StudentForm(FieldControlMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "middle_name", "last_name", "email", "birth_date", "age", "year", "photo"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_control_style()
        self.fields["birth_date"].widget.attrs.update({ "type": "date"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email.endswith("@example.com"):
            raise ValidationError("email should end with @example.com")
        return email

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name and last_name and first_name.lower() == last_name.lower():
            raise ValidationError("first name and last name should not be same")
        return cleaned_data
