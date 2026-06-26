from django.urls import path
from library.apps import LibraryConfig

from library import views

app_name = LibraryConfig.name

urlpatterns = [
    path("index/", views.index, name="index"),

    path("authors_list/", views.authors_list, name="authors_list"),
    path("author_details/<int:pk>/", views.author_details, name="author"),

    path("books_list/", views.books_list, name="books_list"),
    path("book/<int:pk>/", views.book_details, name="book"),
]