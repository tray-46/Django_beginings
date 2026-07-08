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

    path("article/", views.ArticleListView.as_view(), name="article_list"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("article/new/", views.ArticleCreateView.as_view(), name="article_create"),
    path("article/edit/<int:pk>/", views.ArticleUpdateView.as_view(), name="article_edit"),
    path("article/delete/<int:pk>/", views.ArticleDeleteView.as_view(), name="article_delete"),

    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/new/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_edit"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),

    path("articles/contacts/", views.ContactsFormView.as_view(), name="contacts"),
    path("articles/comment/", views.CommentFormView.as_view(), name="comments"),
]
