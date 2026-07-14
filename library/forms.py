from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator

from library.models import Comment, Author, Book

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(f"{value} is not even!")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя", help_text="Введите ваше имя", validators=[MinLengthValidator(5), MaxLengthValidator(100)])
    email = forms.EmailField(required=False, label="Почта", help_text="Введите вашу почту", initial="example@example.com", validators=[])
    message = forms.CharField(widget=forms.Textarea, label="Сообщение", initial="Ваше сообщение")
    number = forms.IntegerField(label="Чётное число", help_text="Введите чётное число", validators=[validate_even])

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email.endswith("@example.com"):
            raise ValidationError(f"{email} should end with '@example.com'")
        return email

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")

        if name and email and "spam" in name:
            self.add_error("name", "'name' should not contain 'spam'")
        return cleaned_data

    def send_email(self):
        print(self.cleaned_data)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "text")


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "birth_date")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": f"Введите {field.label}"})

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        # if Author.objects.filter(first_name=first_name, last_name=last_name).exists():
        #     raise ValidationError(f"Author {first_name} {last_name} already exists!")
        if first_name and last_name:
            qs = Author.objects.filter(first_name=first_name, last_name=last_name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(f"Author {first_name} {last_name} already exists!")
        return cleaned_data


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "publication_data", "cover_art", "description", "author")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": f"Введите {field.label}"})
