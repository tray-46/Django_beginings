from django import forms
from django.core.validators import MinLengthValidator

from library.models import Comment, Author, Book

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя", help_text="Введите ваше имя", validators=[MinLengthValidator(5)])
    email = forms.EmailField(required=False, label="Почта", help_text="Введите вашу почту", initial="example@example.com")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение", initial="Ваше сообщение")

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


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "publication_data", "cover_art", "description", "author")
