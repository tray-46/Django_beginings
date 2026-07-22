from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

from users.forms import CustomUserCreationForm

# Create your views here.
class CustomLoginView(LoginView):
    success_url = reverse_lazy("library:index")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("library:index")


# class RegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = "registration/register.html"
#     success_url = reverse_lazy("library:index")
#
#     @staticmethod
#     def send_welcome_mail(user_mail):
#         subject = "Welcome to our Library"
#         message = "Thank you for registering."
#         recipient_list = [user_mail]
#         send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list)
#
#     def form_valid(self, form):
#         responses = super().form_valid(form)
#         login(self.request, self.object)
#         self.send_welcome_mail(self.object.email)
#         return responses


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("library:index")

    @staticmethod
    def send_welcome_mail(user_mail):
        subject = "Welcome to our Library"
        message = "Thank you for registering."
        recipient_list = [user_mail]
        send_mail(subject, message, "no-reply@it.ivc.vsmpo.ru", recipient_list,)

    def form_valid(self, form):
        # user = form.save()
        # login(self.request, user)
        # self.send_welcome_mail(user.email)
        subject = "Welcome to our Library"
        message = "Thank you for registering."
        send_mail(subject, message, "no-reply@it.ivc.vsmpo.ru", ["atst-box@yandex.ru"], )
        return super().form_valid(form)

