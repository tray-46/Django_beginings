from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.example_view, name="example_view"),
    path("show_data/", views.show_data, name="show_data"),
    path("submit_data/", views.submit_data, name="submit_data"),
    path("item/<int:item_id>/", views.show_item, name="show_item"),
    path("about/", views.show_about, name="show_about"),
    path("contact/", views.contact, name="contact"),
]