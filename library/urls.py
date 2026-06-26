from django.urls import path
from library.apps import LibraryConfig

from library import views

app_name = LibraryConfig.name

urlpatterns = [
    path("books_list", views.books_list, name="books_list"),
    path("book/<int:pk>", views.book_details, name="book"),
]